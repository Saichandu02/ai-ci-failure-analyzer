"""Tests for the CLI interface."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from ai_ci_analyzer.cli import main


@pytest.fixture
def runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def temp_log_file(tmp_path: Path) -> str:
    log_file = tmp_path / "test.log"
    log_file.write_text("ERROR: ModuleNotFoundError: No module named 'requests'\n")
    return str(log_file)


@pytest.fixture
def temp_clean_log_file(tmp_path: Path) -> str:
    log_file = tmp_path / "clean.log"
    log_file.write_text("All tests passed!\nBuild successful.\n")
    return str(log_file)


def test_cli_with_log_file(runner: CliRunner, temp_log_file: str) -> None:
    result = runner.invoke(main, [temp_log_file])
    assert result.exit_code in (0, 1)
    assert "AI CI FAILURE ANALYZER REPORT" in result.output


def test_cli_with_stdin(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--stdin"], input="ERROR: ModuleNotFoundError: No module named 'foo'\n")
    assert result.exit_code in (0, 1)
    assert "AI CI FAILURE ANALYZER REPORT" in result.output


def test_cli_json_format(runner: CliRunner, temp_log_file: str) -> None:
    result = runner.invoke(main, [temp_log_file, "--format", "json"])
    assert result.exit_code in (0, 1)
    data = json.loads(result.output)
    assert "summary" in data


def test_cli_markdown_format(runner: CliRunner, temp_log_file: str) -> None:
    result = runner.invoke(main, [temp_log_file, "--format", "markdown"])
    assert result.exit_code in (0, 1)
    assert "# AI CI Failure Analyzer Report" in result.output


def test_cli_verbose_flag(runner: CliRunner, temp_log_file: str) -> None:
    result = runner.invoke(main, [temp_log_file, "--verbose"])
    assert result.exit_code in (0, 1)


def test_cli_no_args_exits_with_error(runner: CliRunner) -> None:
    result = runner.invoke(main, [])
    assert result.exit_code == 2


def test_cli_clean_log_exits_zero(runner: CliRunner, temp_clean_log_file: str) -> None:
    result = runner.invoke(main, [temp_clean_log_file])
    assert result.exit_code == 0


def test_cli_failure_log_exits_one(runner: CliRunner, temp_log_file: str) -> None:
    result = runner.invoke(main, [temp_log_file])
    assert result.exit_code == 1


def test_cli_nonexistent_file(runner: CliRunner) -> None:
    result = runner.invoke(main, ["/nonexistent/path/to/file.log"])
    assert result.exit_code != 0
