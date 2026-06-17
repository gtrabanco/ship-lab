"""json2csv — convert JSON files to CSV format."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("json2csv")
except PackageNotFoundError:
    __version__ = "unknown"
