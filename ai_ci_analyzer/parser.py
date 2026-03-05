"""Log parser for CI log files."""

from __future__ import annotations

import re

from ai_ci_analyzer.models import CILogEntry

_GH_ACTIONS_TS = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+Z")
_GENERIC_TS = re.compile(r"^\[\d{2}:\d{2}:\d{2}\]")
_LEVEL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("ERROR", re.compile(r"\b(error|exception|failed|failure|fatal)\b", re.IGNORECASE)),
    ("WARNING", re.compile(r"\b(warn(?:ing)?|deprecated)\b", re.IGNORECASE)),
    ("DEBUG", re.compile(r"\b(debug|trace)\b", re.IGNORECASE)),
]


class LogParser:
    """Parses raw CI log text into structured log entries."""

    def parse(self, log_text: str) -> list[CILogEntry]:
        """Parse raw CI log text into a list of CILogEntry objects."""
        entries: list[CILogEntry] = []
        for line_number, line in enumerate(log_text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped:
                continue
            timestamp, message = self._extract_timestamp(stripped)
            level = self._detect_level(message)
            entries.append(
                CILogEntry(
                    timestamp=timestamp,
                    level=level,
                    message=message,
                    line_number=line_number,
                )
            )
        return entries

    def extract_error_sections(self, entries: list[CILogEntry]) -> list[CILogEntry]:
        """Filter entries to only ERROR and WARNING level entries."""
        return [e for e in entries if e.level in ("ERROR", "WARNING")]

    def _extract_timestamp(self, line: str) -> tuple[str | None, str]:
        """Extract timestamp from a log line, returning (timestamp, remaining message)."""
        match = _GH_ACTIONS_TS.match(line)
        if match:
            ts = match.group(0)
            return ts, line[len(ts) :].strip()
        match = _GENERIC_TS.match(line)
        if match:
            ts = match.group(0)
            return ts, line[len(ts) :].strip()
        return None, line

    def _detect_level(self, message: str) -> str:
        """Detect the log level from message content."""
        for level, pattern in _LEVEL_PATTERNS:
            if pattern.search(message):
                return level
        return "INFO"
