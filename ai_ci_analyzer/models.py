"""Data models for the AI CI Failure Analyzer."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class FailureCategory(Enum):
    """Categories of CI failure types."""

    DEPENDENCY = "dependency"
    SYNTAX = "syntax"
    TIMEOUT = "timeout"
    TEST = "test"
    BUILD = "build"
    NETWORK = "network"
    PERMISSION = "permission"
    CONFIGURATION = "configuration"
    RESOURCE = "resource"
    UNKNOWN = "unknown"


@dataclass
class CILogEntry:
    """Represents a single parsed line from a CI log."""

    timestamp: str | None
    level: str
    message: str
    line_number: int


@dataclass
class AnalysisResult:
    """Result of analyzing a single failure pattern match."""

    category: FailureCategory
    root_cause: str
    confidence_score: float
    suggested_fix: str
    relevant_lines: list[str] = field(default_factory=list)


@dataclass
class AnalysisReport:
    """Full analysis report for a CI log."""

    summary: str
    results: list[AnalysisResult]
    metadata: dict[str, Any]
    total_lines: int
    error_count: int
