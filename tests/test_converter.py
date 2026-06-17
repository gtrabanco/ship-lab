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


def test_tab_delimiter() -> None:
    records = [{"a": "1", "b": "2"}]
    out = io.StringIO()
    convert(records, out, delimiter="\t")
    lines = out.getvalue().splitlines()
    assert lines[0] == "a\tb"
    assert lines[1] == "1\t2"


def test_semicolon_delimiter() -> None:
    records = [{"a": "1", "b": "2"}]
    out = io.StringIO()
    convert(records, out, delimiter=";")
    lines = out.getvalue().splitlines()
    assert lines[0] == "a;b"
    assert lines[1] == "1;2"


def test_default_delimiter() -> None:
    records = [{"x": "1", "y": "2"}]
    out = io.StringIO()
    convert(records, out)
    assert out.getvalue().splitlines()[0] == "x,y"


def test_package_importable() -> None:
    import json2csv

    assert json2csv.__version__ == "0.0.1"


# --- feature 04: nested-flatten ---


def test_flatten_single_level() -> None:
    records = [{"user": {"name": "Ann", "age": 3}}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "user.name,user.age"
    assert lines[1] == "Ann,3"


def test_flatten_deep() -> None:
    records = [{"a": {"b": {"c": 1}}}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "a.b.c"
    assert lines[1] == "1"


def test_flatten_mixed_flat_and_nested() -> None:
    records = [{"id": 1, "meta": {"tag": "x"}}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "id,meta.tag"
    assert lines[1] == "1,x"


def test_flatten_list_as_json_cell() -> None:
    import csv as _csv

    records = [{"tags": ["a", "b"]}]
    out = io.StringIO()
    convert(records, out)
    out.seek(0)
    reader = _csv.reader(out)
    header = next(reader)
    row = next(reader)
    assert header == ["tags"]
    assert row == ['["a", "b"]']


def test_flatten_mismatched_shapes() -> None:
    records = [{"user": {"name": "Ann"}}, {"user": {"name": "Bob", "age": 30}}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "user.name,user.age"
    assert lines[1] == "Ann,"
    assert lines[2] == "Bob,30"


def test_flat_only_unchanged() -> None:
    records = [{"name": "Alice", "age": "30"}, {"name": "Bob", "age": "25"}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "name,age"
    assert lines[1] == "Alice,30"
    assert lines[2] == "Bob,25"


def test_flatten_leaf_normalization() -> None:
    records = [{"meta": {"active": True, "deleted": False, "note": None}}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines[0] == "meta.active,meta.deleted,meta.note"
    assert lines[1] == "true,false,"


def test_flatten_empty_nested_object() -> None:
    records = [{"a": {}}]
    out = io.StringIO()
    convert(records, out)
    assert out.getvalue() == ""


def test_top_level_empty_object_skipped() -> None:
    records = [{}, {"b": 1}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines == ["b", "1"]


def test_flatten_empty_nested_object_mixed() -> None:
    records = [{"a": {}}, {"b": 1}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines == ["b", "1"]


def test_flatten_partial_empty_nested_keeps_row() -> None:
    records = [{"a": {}, "b": 1}, {"b": 2}]
    out = io.StringIO()
    convert(records, out)
    lines = out.getvalue().splitlines()
    assert lines == ["b", "1", "2"]
