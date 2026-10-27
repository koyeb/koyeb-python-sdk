"""The pure diff engine behind filesystem.sync().

sync() is one-way like ``rsync -r`` without deltas: list both sides (a
local walk against GET /files/list NDJSON), diff on path/type/size/mtime
(+sha256 with checksum=True), and send the changed set as ~50 MiB tar
batches through /files/archive. This module holds the decisions — walking,
matching, diffing, planning — with no executor I/O, so every rule is
testable against plain data and tmpdir trees.

The wire shape on both sides is the executor's FileEntry: ``path``
(relative, /-separated), ``type`` (file|dir|symlink|other), ``size``,
``mode`` (4-digit octal permission bits), ``mtime`` (RFC 3339 UTC with
nanoseconds). Exclude patterns follow the executor's archive-route
semantics exactly — Go's path.Match, tried against the relative path and
every /-separated suffix of it — so the local walk and the remote
archive agree on what is in the tree.
"""

import os
import posixpath
import shutil
import stat as stat_module
import tarfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, Iterable, List, Optional, Sequence, Set, Tuple

__all__ = [
    "SYNC_BATCH_BYTES",
    "SyncDiff",
    "build_archive",
    "diff",
    "excluded",
    "extract_archive",
    "format_mtime",
    "hash_candidates",
    "join_local",
    "mtime_seconds",
    "path_match",
    "plan_batches",
    "prune_descendants",
    "relative_remote",
    "remote_join",
    "walk_local",
]

# One tar batch's raw content budget: the multipart part size (50 MiB),
# comfortably inside the 100 MiB body cap with tar/gzip overhead on top.
SYNC_BATCH_BYTES = 50 * 1024 * 1024


# --------------------------------------------------------------------------
# Go path.Match parity
#
# The executor applies exclude patterns with Go's path.Match, where '*' and
# '?' never cross the '/' separator. fnmatch is looser ('*' crosses '/'), so
# the semantics are ported faithfully; a malformed pattern raises
# ValueError the way the executor answers 400.

def _scan_chunk(pattern: str) -> Tuple[bool, str, str]:
    """Whether the chunk starts with *, the chunk, and the rest. (Go scanChunk.)

    The chunk ends at an unescaped '*' outside a character class;
    leading stars all collapse into the flag.
    """
    star = pattern.startswith("*")
    while pattern.startswith("*"):
        pattern = pattern[1:]
        star = True
    inrange = False
    i = 0
    n = len(pattern)
    while i < n:
        c = pattern[i]
        if c == "\\":
            # A bad trailing escape is matchChunk's error to report.
            if i + 1 < n:
                i += 1
        elif c == "[":
            inrange = True
        elif c == "]":
            inrange = False
        elif c == "*" and not inrange:
            break
        i += 1
    return star, pattern[:i], pattern[i:]


def _get_esc(chunk: str) -> Tuple[str, str]:
    """One class member: a literal, or a \\-escaped character. (Go getEsc.)"""
    if not chunk or chunk[0] in ("-", "]", "\\"):
        raise ValueError(f"bad exclude pattern")
    if chunk[0] == "\\":
        chunk = chunk[1:]
        if not chunk:
            raise ValueError(f"bad exclude pattern")
    return chunk[0], chunk[1:]


def _match_chunk(chunk: str, s: str) -> Tuple[str, bool]:
    """Match one pattern chunk at the head of s. (Go matchChunk.)

    Returns (rest-of-s, matched); raises ValueError on a malformed chunk.
    After the match fails the chunk is still validated, exactly like Go.
    """
    failed = False
    while chunk:
        if not failed and not s:
            failed = True
        c, chunk = chunk[0], chunk[1:]
        if c == "[":
            if not failed:
                r, s = s[0], s[1:]
            else:
                r = ""
            negated = chunk.startswith("^")
            if negated:
                chunk = chunk[1:]
            matched = False
            nrange = 0
            while True:
                if chunk.startswith("]") and nrange > 0:
                    chunk = chunk[1:]
                    break
                lo, chunk = _get_esc(chunk)
                hi = lo
                if chunk.startswith("-"):
                    hi, chunk = _get_esc(chunk[1:])
                if lo <= r <= hi:
                    matched = True
                nrange += 1
            if matched == negated:
                failed = True
        elif c == "?":
            if not failed:
                if s[:1] == "/":
                    failed = True
                s = s[1:]
        elif c == "\\":
            if not chunk:
                raise ValueError(f"bad exclude pattern")
            if not failed:
                if chunk[0] != s[:1]:
                    failed = True
                s = s[1:]
            chunk = chunk[1:]
        else:
            if not failed:
                if c != s[:1]:
                    failed = True
                s = s[1:]
    return s, not failed


def path_match(pattern: str, name: str) -> bool:
    """Go's path.Match: '*', '?' and [...] never cross the '/' separator."""
    while pattern:
        star, chunk, pattern = _scan_chunk(pattern)
        if star and not chunk:
            # A trailing * matches the rest unless it has a separator.
            return "/" not in name
        rest, ok = _match_chunk(chunk, name)
        if ok and (not rest or pattern):
            name = rest
            continue
        if star:
            # Look for a match skipping i+1 bytes of the name.
            matched_at = None
            i = 0
            while i < len(name) and name[i] != "/":
                rest, ok = _match_chunk(chunk, name[i + 1 :])
                if ok:
                    if not pattern and rest:
                        i += 1
                        continue
                    matched_at = rest
                    break
                i += 1
            if matched_at is not None:
                name = matched_at
                continue
        # Before returning False, validate the rest of the pattern.
        while pattern:
            _, chunk, pattern = _scan_chunk(pattern)
            _match_chunk(chunk, "")
        return False
    return not name


def excluded(rel: str, patterns: Sequence[str]) -> bool:
    """The executor's exclude rule: pattern against rel and every suffix.

    A directory that matches is pruned whole by the walker, so its
    descendants never reach this test — matching the archive route, which
    answers SkipDir at the same point.
    """
    for pattern in patterns:
        name = rel
        while True:
            if path_match(pattern, name):
                return True
            i = name.find("/")
            if i < 0:
                break
            name = name[i + 1 :]
    return False


# --------------------------------------------------------------------------
# mtime formatting
#
# The executor writes RFC 3339 with nanoseconds (RFC3339Nano, trailing
# zeros trimmed); the diff compares whole seconds, because tar's PAX mtime
# cannot round-trip nanosecond precision — the same default as rsync.

def format_mtime(ns: int) -> str:
    """Nanoseconds since the epoch as the executor formats mtime."""
    seconds, nanos = divmod(ns, 1_000_000_000)
    dt = datetime.fromtimestamp(seconds, tz=timezone.utc)
    base = f"{dt:%Y-%m-%dT%H:%M:%S}"
    if nanos:
        frac = f"{nanos:09d}".rstrip("0")
        return f"{base}.{frac}Z"
    return f"{base}Z"


def mtime_seconds(mtime: str) -> int:
    """An RFC 3339 mtime as whole seconds since the epoch (floored)."""
    base, _, _ = mtime.rstrip("Z").partition(".")
    dt = datetime.strptime(base, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


# --------------------------------------------------------------------------
# local walk

def _rel_path(root: str, dirpath: str, name: str) -> str:
    rel = os.path.relpath(os.path.join(dirpath, name), root)
    return rel.replace(os.sep, "/")


def _classify(st_mode: int) -> Optional[str]:
    if stat_module.S_ISREG(st_mode):
        return "file"
    if stat_module.S_ISDIR(st_mode):
        return "dir"
    if stat_module.S_ISLNK(st_mode):
        return "symlink"
    return None  # devices, FIFOs, sockets: not archivable


def _entry(path: str, type_: str, st: os.stat_result) -> Dict[str, Any]:
    return {
        "path": path,
        "type": type_,
        "size": st.st_size,
        "mode": f"{stat_module.S_IMODE(st.st_mode):04o}",
        "mtime": format_mtime(st.st_mtime_ns),
    }


def walk_local(root: str, exclude: Sequence[str] = ()) -> List[Dict[str, Any]]:
    """A local tree as FileEntry dicts, mirroring GET /files/list.

    Paths are relative to root and /-separated; the root itself is not an
    entry. Symlinks are listed, not followed (like the executor's walk),
    special files are skipped, and an excluded directory is pruned whole.
    """
    entries: List[Dict[str, Any]] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames.sort()
        filenames.sort()
        kept: List[str] = []
        for name in dirnames:
            rel = _rel_path(root, dirpath, name)
            if excluded(rel, exclude):
                continue
            kept.append(name)
            st = os.lstat(os.path.join(dirpath, name))
            type_ = _classify(st.st_mode) or "dir"
            entries.append(_entry(rel, type_, st))
        dirnames[:] = kept
        for name in filenames:
            rel = _rel_path(root, dirpath, name)
            if excluded(rel, exclude):
                continue
            st = os.lstat(os.path.join(dirpath, name))
            type_ = _classify(st.st_mode)
            if type_ is None:
                continue
            entries.append(_entry(rel, type_, st))
    return entries


# --------------------------------------------------------------------------
# diff

@dataclass
class SyncDiff:
    """What sync() must do with one pair of trees, before any transfer.

    to_transfer holds source entries (walk order) to copy; deletes holds
    destination entries absent from the source; skipped counts entries
    examined and left alone; bytes is the content bytes to move.
    """

    to_transfer: List[Dict[str, Any]] = field(default_factory=list)
    deletes: List[Dict[str, Any]] = field(default_factory=list)
    skipped: int = 0
    bytes: int = 0


def diff(
    local_entries: Iterable[Dict[str, Any]],
    remote_entries: Iterable[Dict[str, Any]],
    *,
    delete: bool = False,
    local_hash: Optional[Callable[[str], str]] = None,
    remote_hash: Optional[Callable[[str], Optional[str]]] = None,
) -> SyncDiff:
    """Diff two FileEntry trees and plan a one-way copy.

    An entry is unchanged when type, size and mtime (whole seconds) match
    on both sides. With hashing callables, files that pass that test are
    compared by sha256 too (checksum=True); a remote hash of None can't
    prove a change and skips. Unreadable remote entries (the ``error``
    field) and unarchivable types (``other``) are never transfer
    candidates.
    """
    checksum = local_hash is not None and remote_hash is not None
    result = SyncDiff()
    remote = {e["path"]: e for e in remote_entries}
    for entry in local_entries:
        if entry.get("type") == "other":
            result.skipped += 1
            continue
        path = entry["path"]
        remote_entry = remote.pop(path, None)
        if remote_entry is None:
            _count(result, entry)
            continue
        if "error" in remote_entry or remote_entry.get("type") == "other":
            result.skipped += 1
            continue
        if _changed(entry, remote_entry):
            _count(result, entry)
            continue
        if checksum and entry["type"] == "file":
            remote_digest = remote_hash(path)
            if remote_digest is not None and remote_digest != local_hash(path):
                _count(result, entry)
            else:
                result.skipped += 1
            continue
        result.skipped += 1
    if delete:
        result.deletes = [e for p, e in remote.items() if "error" not in e]
    else:
        result.skipped += sum(1 for e in remote.values())
    return result


def _changed(local_entry: Dict[str, Any], remote_entry: Dict[str, Any]) -> bool:
    if local_entry["type"] != remote_entry.get("type"):
        return True
    if local_entry.get("size", 0) != remote_entry.get("size", 0):
        return True
    if mtime_seconds(local_entry.get("mtime", "")) != mtime_seconds(
        remote_entry.get("mtime", "")
    ):
        return True
    return False


def hash_candidates(
    source_entries: Iterable[Dict[str, Any]],
    dest_entries: Iterable[Dict[str, Any]],
) -> List[str]:
    """Paths that only a sha256 comparison can settle.

    Files present on both sides, matching on type, size and mtime: the
    candidates checksum=True must hash. The caller prefetches the
    executor-side digests for these in one pass (async has no other way
    to feed the pure, synchronous diff).
    """
    dest = {e["path"]: e for e in dest_entries}
    candidates: List[str] = []
    for entry in source_entries:
        other = dest.get(entry["path"])
        if (
            entry.get("type") == "file"
            and other is not None
            and other.get("type") == "file"
            and not _changed(entry, other)
        ):
            candidates.append(entry["path"])
    return candidates


def _count(result: SyncDiff, entry: Dict[str, Any]) -> None:
    result.to_transfer.append(entry)
    if entry["type"] == "file":
        result.bytes += entry.get("size", 0)


# --------------------------------------------------------------------------
# batch planning

def plan_batches(
    entries: Sequence[Dict[str, Any]], part_size: int
) -> Tuple[List[List[Dict[str, Any]]], List[Dict[str, Any]]]:
    """Cut the changed set into tar batches and oversized files.

    Batches accumulate raw file content up to part_size (~50 MiB): a
    file that would cross the boundary starts the next batch, so no file
    is ever split across archives. Files larger than one part go through
    upload_file/download_file instead. Directories and symlinks ride the
    next batch (their wire size is a header); a set of only those still
    produces one batch.
    """
    batches: List[List[Dict[str, Any]]] = []
    oversized: List[Dict[str, Any]] = []
    current: List[Dict[str, Any]] = []
    current_bytes = 0
    for entry in entries:
        size = entry.get("size", 0)
        if entry["type"] == "file" and size > part_size:
            oversized.append(entry)
            continue
        if current and current_bytes + size > part_size:
            batches.append(current)
            current = []
            current_bytes = 0
        current.append(entry)
        current_bytes += size
    if current:
        batches.append(current)
    return batches, oversized


# --------------------------------------------------------------------------
# deletes and the remote default

def remote_join(remote: str, rel: str) -> str:
    """A remote path for a relative entry path (remote paths are POSIX)."""
    return posixpath.join(remote, rel)


def join_local(root: str, rel: str) -> str:
    """A local path for a relative entry path, on any platform."""
    return os.path.join(root, *rel.split("/"))


def prune_descendants(paths: Sequence[str]) -> List[str]:
    """Topmost paths only: deleting a directory takes its descendants.

    Input order is irrelevant; the result is sorted. A descendant of a
    kept path is already covered by its parent's recursive delete, and
    deleting it separately would just miss (it is already gone).
    """
    kept: List[str] = []
    for path in sorted(paths):
        if kept and path.startswith(kept[-1] + "/"):
            continue
        kept.append(path)
    return kept


def relative_remote(local: str) -> str:
    """The remote path used when remote=None: local's relative form.

    A relative local path is kept as-is (resolved by the executor against
    the sandbox workdir); an absolute one contributes its basename,
    rsync-style.
    """
    normalized = os.path.normpath(local)
    if os.path.isabs(normalized):
        normalized = os.path.basename(normalized)
    return normalized.replace(os.sep, "/")


# --------------------------------------------------------------------------
# tar batches
#
# A batch is built spooled to disk, then streamed into PUT /files/archive
# (constant memory, bounded disk: one batch ~ part_size). PAX headers keep
# long names working; mtimes are whole seconds, exactly what the diff
# compares. Owners are not kept (uid/gid 0), per the design.

def _tar_member(entry: Dict[str, Any]) -> "tarfile.TarInfo":
    info = tarfile.TarInfo(entry["path"])
    info.mode = int(entry["mode"], 8)
    info.mtime = mtime_seconds(entry["mtime"])
    info.uid = 0
    info.gid = 0
    if entry["type"] == "dir":
        info.type = tarfile.DIRTYPE
        info.size = 0
    elif entry["type"] == "symlink":
        info.type = tarfile.SYMTYPE
        info.size = 0
    else:
        info.type = tarfile.REGTYPE
        info.size = entry["size"]
    return info


def build_archive(
    root: str, entries: Sequence[Dict[str, Any]], dest: str
) -> None:
    """Write the changed entries as a gzip'd tar spooled to dest.

    Members mirror the executor's archive: paths relative and
    /-separated, modes and whole-second mtimes kept, symlinks as links.
    """
    with tarfile.open(dest, "w:gz", format=tarfile.PAX_FORMAT) as tar:
        for entry in entries:
            info = _tar_member(entry)
            if entry["type"] == "symlink":
                full = os.path.join(root, *entry["path"].split("/"))
                info.linkname = os.readlink(full)
                tar.addfile(info)
            elif entry["type"] == "dir":
                tar.addfile(info)
            else:
                full = os.path.join(root, *entry["path"].split("/"))
                with open(full, "rb") as f:
                    tar.addfile(info, f)


def _clean_member(name: str) -> str:
    """A member path safe to write under the destination, or ValueError.

    The same refusal the executor applies to archives it extracts:
    absolute paths and .. escapes never touch the filesystem.
    """
    normalized = posixpath.normpath(name)
    if normalized.startswith("/") or normalized == ".." or normalized.startswith("../"):
        raise ValueError(f"refusing archive member outside destination: {name!r}")
    return normalized


def extract_archive(
    archive_path: str, dest: str, keep: Optional[Set[str]] = None
) -> List[str]:
    """Extract a spooled archive into dest, mirroring the executor.

    Missing parents are created; members in the way are replaced;
    directory modes and mtimes are applied after the contents (writing
    into a directory bumps its mtime, and a restrictive mode applied
    early would lock the contents out). With keep, only those members are
    extracted — the pull side's changed set. Returns the member paths
    extracted.
    """
    extracted: List[str] = []
    dirs: List[Tuple[str, int, int]] = []
    with tarfile.open(archive_path, "r:gz") as tar:
        for member in tar:
            name = _clean_member(member.name)
            if keep is not None and name not in keep:
                continue
            path = os.path.join(dest, *name.split("/"))
            if member.isdir():
                os.makedirs(path, exist_ok=True)
                dirs.append((path, member.mode, int(member.mtime)))
            elif member.issym():
                if os.path.lexists(path) and not os.path.isdir(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path)
                os.makedirs(os.path.dirname(path), exist_ok=True)
                os.symlink(member.linkname, path)
            elif member.isfile():
                os.makedirs(os.path.dirname(path), exist_ok=True)
                source = tar.extractfile(member)
                if source is None:
                    continue
                with open(path, "wb") as out:
                    shutil.copyfileobj(source, out, 1 << 20)
                os.chmod(path, member.mode)
                os.utime(path, (int(member.mtime), int(member.mtime)))
            else:
                continue
            extracted.append(name)
    # Directory modes and mtimes last, deepest first, like the executor.
    for path, mode, mtime in sorted(dirs, key=lambda d: d[0], reverse=True):
        os.chmod(path, mode)
        os.utime(path, (mtime, mtime))
    return extracted
