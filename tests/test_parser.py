"""Tests for LogParser."""

from __future__ import annotations

from ai_ci_analyzer.models import CILogEntry
from ai_ci_analyzer.parser import LogParser


def test_parse_simple_log(parser: LogParser) -> None:
    log = "Step 1: Running tests\nERROR: Test failed\n"
    entries = parser.parse(log)
    assert len(entries) == 2


def test_parse_empty_log(parser: LogParser) -> None:
    entries = parser.parse("")
    assert entries == []


def test_parse_skips_blank_lines(parser: LogParser) -> None:
    log = "line1\n\n\nline2\n"
    entries = parser.parse(log)
    assert len(entries) == 2


def test_parse_assigns_line_numbers(parser: LogParser) -> None:
    log = "line1\nline2\nline3\n"
    entries = parser.parse(log)
    assert entries[0].line_number == 1
    assert entries[1].line_number == 2
    assert entries[2].line_number == 3


def test_parse_detects_error_level(parser: LogParser) -> None:
    log = "ERROR: Something failed\n"
    entries = parser.parse(log)
    assert entries[0].level == "ERROR"


def test_parse_detects_warning_level(parser: LogParser) -> None:
    log = "WARNING: Something is deprecated\n"
    entries = parser.parse(log)
    assert entries[0].level == "WARNING"


def test_parse_detects_info_level(parser: LogParser) -> None:
    log = "Step completed successfully\n"
    entries = parser.parse(log)
    assert entries[0].level == "INFO"


def test_parse_extracts_github_actions_timestamp(parser: LogParser) -> None:
    log = "2024-01-15T10:30:00.000Z Running step\n"
    entries = parser.parse(log)
    assert entries[0].timestamp == "2024-01-15T10:30:00.000Z"
    assert "Running step" in entries[0].message


def test_parse_extracts_generic_timestamp(parser: LogParser) -> None:
    log = "[10:30:00] Running step\n"
    entries = parser.parse(log)
    assert entries[0].timestamp == "[10:30:00]"
    assert "Running step" in entries[0].message


def test_parse_no_timestamp(parser: LogParser) -> None:
    log = "Some message without timestamp\n"
    entries = parser.parse(log)
    assert entries[0].timestamp is None


def test_extract_error_sections(parser: LogParser) -> None:
    entries = [
        CILogEntry(timestamp=None, level="INFO", message="info", line_number=1),
        CILogEntry(timestamp=None, level="ERROR", message="error", line_number=2),
        CILogEntry(timestamp=None, level="WARNING", message="warning", line_number=3),
        CILogEntry(timestamp=None, level="DEBUG", message="debug", line_number=4),
    ]
    error_sections = parser.extract_error_sections(entries)
    assert len(error_sections) == 2
    assert all(e.level in ("ERROR", "WARNING") for e in error_sections)


def test_parse_multiline_log(parser: LogParser) -> None:
    log = "\n".join(
        [
            "2024-01-15T10:00:00.000Z Starting build",
            "Installing dependencies",
            "ERROR: ModuleNotFoundError: No module named 'requests'",
            "Build failed",
        ]
    )
    entries = parser.parse(log)
    assert len(entries) == 4
    assert entries[0].timestamp == "2024-01-15T10:00:00.000Z"
    assert entries[2].level == "ERROR"
