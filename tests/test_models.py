"""Tests for data models."""

from __future__ import annotations

from ai_ci_analyzer.models import (
    AnalysisReport,
    AnalysisResult,
    CILogEntry,
    FailureCategory,
)


def test_failure_category_values() -> None:
    assert FailureCategory.DEPENDENCY.value == "dependency"
    assert FailureCategory.SYNTAX.value == "syntax"
    assert FailureCategory.TIMEOUT.value == "timeout"
    assert FailureCategory.TEST.value == "test"
    assert FailureCategory.BUILD.value == "build"
    assert FailureCategory.NETWORK.value == "network"
    assert FailureCategory.PERMISSION.value == "permission"
    assert FailureCategory.CONFIGURATION.value == "configuration"
    assert FailureCategory.RESOURCE.value == "resource"
    assert FailureCategory.UNKNOWN.value == "unknown"


def test_ci_log_entry_creation() -> None:
    entry = CILogEntry(timestamp="2024-01-01T00:00:00Z", level="ERROR", message="Error occurred", line_number=1)
    assert entry.timestamp == "2024-01-01T00:00:00Z"
    assert entry.level == "ERROR"
    assert entry.message == "Error occurred"
    assert entry.line_number == 1


def test_ci_log_entry_no_timestamp() -> None:
    entry = CILogEntry(timestamp=None, level="INFO", message="info message", line_number=5)
    assert entry.timestamp is None


def test_analysis_result_defaults() -> None:
    result = AnalysisResult(
        category=FailureCategory.DEPENDENCY,
        root_cause="Missing module",
        confidence_score=0.9,
        suggested_fix="pip install",
    )
    assert result.relevant_lines == []
    assert result.category == FailureCategory.DEPENDENCY


def test_analysis_result_with_lines() -> None:
    result = AnalysisResult(
        category=FailureCategory.TEST,
        root_cause="Test failed",
        confidence_score=0.8,
        suggested_fix="Fix the test",
        relevant_lines=["line1", "line2"],
    )
    assert len(result.relevant_lines) == 2


def test_analysis_report_creation() -> None:
    result = AnalysisResult(
        category=FailureCategory.BUILD,
        root_cause="Build error",
        confidence_score=0.7,
        suggested_fix="Fix build",
    )
    report = AnalysisReport(
        summary="1 failure detected",
        results=[result],
        metadata={"version": "1.0.0"},
        total_lines=100,
        error_count=5,
    )
    assert report.total_lines == 100
    assert report.error_count == 5
    assert len(report.results) == 1
    assert report.summary == "1 failure detected"
