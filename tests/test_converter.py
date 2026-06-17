"""Smoke tests for the converter module (stub phase)."""

import json2csv


def test_package_importable() -> None:
    assert json2csv.__version__ == "0.0.1"
