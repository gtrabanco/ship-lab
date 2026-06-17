"""Tests for converter.py — pure conversion logic."""

import io

from json2csv.converter import convert


def test_flat_objects() -> None:
    records = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "name,age"
    assert lines[1] == "Alice,30"
    assert lines[2] == "Bob,25"


def test_empty_array() -> None:
    out = io.StringIO()
    convert([], out)
    assert out.getvalue() == ""


def test_mismatched_keys() -> None:
    records = [{"a": "1", "b": "2"}, {"b": "3", "c": "4"}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "a,b,c"
    assert lines[1] == "1,2,"
    assert lines[2] == ",3,4"


def test_boolean_normalization() -> None:
    records = [{"flag": True, "off": False, "empty": None}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "flag,off,empty"
    assert lines[1] == "true,false,"


def test_package_importable() -> None:
    import json2csv

    assert json2csv.__version__ == "0.0.1"
