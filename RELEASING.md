# Releasing

`main` always carries the version of the next release. Pushing a `vX.Y.Z` tag publishes that commit to PyPI through [release.yml](.github/workflows/release.yml); the published version is the one in `pyproject.toml` at the tagged commit.

1. If the next release needs a minor or major bump instead of the patch bump already on `main`, open a PR with `bumpver update --minor` (or `--major`) and merge it.
2. Tag the commit on `main` and push the tag:
   ```bash
   git tag vX.Y.Z <commit> && git push origin vX.Y.Z
   ```
   The tagged version must match `pyproject.toml`, and must not already be on PyPI.
3. Open a "Post release version bump" PR so `main` carries the next version:
   ```bash
   bumpver update --patch
   ```

`bumpver` (configured in `bumpver.toml`) does not touch `uv.lock`: run `uv lock` as well, or set the `koyeb-sdk` package version in `uv.lock` by hand, and check the diff only changes that line.
