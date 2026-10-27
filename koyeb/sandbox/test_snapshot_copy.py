"""Pins DeclarativeSnapshot's copy onto the new routes.

``copy`` moves a local file or directory into the builder sandbox:
directories travel as one archive push (binary-safe, modes/mtimes/symlinks
kept) on executors v0.0.24+, single files through the streamed
upload_file — with the legacy per-file walk preserved for old executors.
"""

import os
import tempfile
import unittest

from koyeb.sandbox.snapshot import DeclarativeSnapshot


class _FakeFS:
    def __init__(self, new_routes):
        self.new_routes = new_routes
        self.calls = []

    def _get_client(self):
        return self

    def has_files_routes(self):
        return self.new_routes

    def sync(self, local, remote, **kwargs):
        self.calls.append(("sync", local, remote))
        return {"uploaded": 0, "deleted": 0, "skipped": 0, "bytes": 0}

    def upload_file(self, local, remote, **kwargs):
        self.calls.append(("upload_file", local, remote))

    def mkdir(self, path):
        self.calls.append(("mkdir", path))

    def write_file(self, path, content, encoding="utf-8"):
        self.calls.append(("write_file", path, content, encoding))


class _FakeBuilderSandbox:
    def __init__(self, fs):
        self.filesystem = fs


class SnapshotCopyTestCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.base = self._tmp.name
        self.addCleanup(self._tmp.cleanup)
        self.snap = DeclarativeSnapshot(
            name="t", image="img", api_token="token"
        )

    def _fs(self, new_routes):
        fs = _FakeFS(new_routes)
        self.snap._builder_sandbox = _FakeBuilderSandbox(fs)
        return fs

    def _tree(self):
        # Text-only contents: the legacy arm reads files as text, exactly
        # as it always did — the binary-safety of the new arms is
        # upload_file/sync's own tested property.
        root = os.path.join(self.base, "src")
        os.makedirs(os.path.join(root, "sub"))
        with open(os.path.join(root, "a.txt"), "wb") as f:
            f.write(b"hello")
        with open(os.path.join(root, "sub", "b.txt"), "wb") as f:
            f.write(b"world")
        return root


class TestCopyDirectory(SnapshotCopyTestCase):
    def test_new_routes_pushes_one_archive(self):
        src = self._tree()
        fs = self._fs(new_routes=True)

        self.snap._copy(src, "dst")

        self.assertEqual(
            [c[0] for c in fs.calls],
            ["sync"],
        )
        self.assertEqual(fs.calls[0][1:], (src, "dst"))

    def test_legacy_walks_per_file(self):
        src = self._tree()
        fs = self._fs(new_routes=False)

        self.snap._copy(src, "dst")

        methods = [c[0] for c in fs.calls]
        self.assertNotIn("sync", methods)
        self.assertIn("mkdir", methods)
        self.assertEqual(methods.count("write_file"), 2)
        written = {c[1]: c[2] for c in fs.calls if c[0] == "write_file"}
        self.assertEqual(written["dst/a.txt"], "hello")

    def test_legacy_walk_reads_text_like_before(self):
        # The legacy arm keeps its historical shape: directories created,
        # files read as text. Unchanged behavior for old executors.
        src = self._tree()
        fs = self._fs(new_routes=False)

        self.snap._copy(src, "dst")

        made = [c[1] for c in fs.calls if c[0] == "mkdir"]
        # The root itself was never an explicit mkdir: make_dir's MkdirAll
        # semantics create it as a parent — unchanged legacy behavior.
        self.assertEqual(made, ["dst/sub"])


class TestCopySingleFile(SnapshotCopyTestCase):
    def test_uploads_streamed_binary_safe(self):
        src = os.path.join(self.base, "one.bin")
        with open(src, "wb") as f:
            f.write(b"\x00\x01")
        fs = self._fs(new_routes=True)

        self.snap._copy(src, "dst/one.bin")

        self.assertEqual(
            fs.calls,
            [("upload_file", src, "dst/one.bin")],
        )

    def test_single_file_uploads_on_legacy_too(self):
        # upload_file carries its own legacy fallback; no probe needed.
        src = os.path.join(self.base, "one.txt")
        with open(src, "w") as f:
            f.write("text")
        fs = self._fs(new_routes=False)

        self.snap._copy(src, "dst/one.txt")

        self.assertEqual(
            fs.calls,
            [("upload_file", src, "dst/one.txt")],
        )


if __name__ == "__main__":
    unittest.main()
