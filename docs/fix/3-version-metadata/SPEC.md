# SPEC — fix/3 version-metadata

**Issue:** #3 · **Branch:** fix/3-version-metadata · **Status:** in-progress

## Problem

`src/json2csv/__init__.py` hardcodes `__version__ = "0.0.1"`. When the version
is bumped in `pyproject.toml` for a release, `__init__.py` must be updated
manually — they can silently drift. The canonical Python packaging pattern is to
read the version from the installed package metadata at import time.

## Fix

Replace the hardcoded string with a `importlib.metadata.version()` call and a
`PackageNotFoundError` fallback for editable / source-tree installs where metadata
may not be present:

```python
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("json2csv")
except PackageNotFoundError:
    __version__ = "unknown"
```

`importlib.metadata` is stdlib since Python 3.8 — no new dependency.

## Acceptance criteria

1. `json2csv.__version__` returns the version declared in `pyproject.toml` when
   the package is installed (including editable `pip install -e .`).
2. `json2csv.__version__` returns `"unknown"` when the package is not installed
   (source-tree import without install).
3. The existing `test_package_importable` test still passes.
4. `ruff check . && pytest` exits 0.

## Out of scope

Bumping the version number itself; publishing to PyPI; CI release workflow.
