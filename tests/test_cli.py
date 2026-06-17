"""CLI integration tests."""

import json

from click.testing import CliRunner

from json2csv.cli import main


def test_cli_help() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output


def test_cli_file_arg() -> None:
    runner = CliRunner()
    data = [{"x": "1", "y": "2"}]
    with runner.isolated_filesystem():
        with open("in.json", "w") as f:
            json.dump(data, f)
        result = runner.invoke(main, ["in.json"])
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert lines[0] == "x,y"
    assert lines[1] == "1,2"


def test_cli_stdin() -> None:
    runner = CliRunner()
    data = json.dumps([{"a": "hello"}])
    result = runner.invoke(main, input=data)
    assert result.exit_code == 0
    lines = result.output.splitlines()
    assert lines[0] == "a"
    assert lines[1] == "hello"


def test_cli_output_flag() -> None:
    runner = CliRunner()
    data = [{"k": "v"}]
    with runner.isolated_filesystem():
        with open("in.json", "w") as f:
            json.dump(data, f)
        result = runner.invoke(main, ["in.json", "-o", "out.csv"])
        assert result.exit_code == 0
        with open("out.csv") as f:
            lines = f.read().splitlines()
        assert lines[0] == "k"
        assert lines[1] == "v"


def test_invalid_json() -> None:
    runner = CliRunner()
    result = runner.invoke(main, input="not json at all")
    assert result.exit_code != 0


def test_non_object_array() -> None:
    runner = CliRunner()
    result = runner.invoke(main, input="[1, 2, 3]")
    assert result.exit_code != 0
    assert "non-object" in result.output.lower() or "object" in result.output.lower()
