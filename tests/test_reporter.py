"""Tests for ReportFormatter."""

from __future__ import annotations

import json

import pytest

from ai_ci_analyzer.models import AnalysisReport, AnalysisResult, FailureCategory
from ai_ci_analyzer.reporter import ReportFormatter


@pytest.fixture
def sample_report() -> AnalysisReport:
    return AnalysisReport(
        summary="Detected 1 failure(s) in categories: dependency.",
        results=[
            AnalysisResult(
                category=FailureCategory.DEPENDENCY,
                root_cause="Python module not found",
                confidence_score=0.9,
                suggested_fix="Run pip install",
                relevant_lines=["ModuleNotFoundError: No module named 'requests'"],
            )
        ],
        metadata={"analyzer_version": "1.0.0", "patterns_checked": 40, "timestamp": "2024-01-01T00:00:00+00:00"},
        total_lines=10,
        error_count=2,
    )


@pytest.fixture
def empty_report() -> AnalysisReport:
    return AnalysisReport(
        summary="No failures detected in the CI log.",
        results=[],
        metadata={"analyzer_version": "1.0.0", "patterns_checked": 40, "timestamp": "2024-01-01T00:00:00+00:00"},
        total_lines=5,
        error_count=0,
    )


def test_format_text_contains_summary(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_text(sample_report)
    assert "Detected 1 failure" in output


def test_format_text_contains_category(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_text(sample_report)
    assert "dependency" in output


def test_format_text_contains_confidence(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_text(sample_report)
    assert "90%" in output


def test_format_text_contains_fix(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_text(sample_report)
    assert "pip install" in output


def test_format_text_contains_relevant_lines(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_text(sample_report)
    assert "requests" in output


def test_format_text_empty_report(formatter: ReportFormatter, empty_report: AnalysisReport) -> None:
    output = formatter.format_text(empty_report)
    assert "No failures detected" in output


def test_format_json_is_valid(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_json(sample_report)
    data = json.loads(output)
    assert isinstance(data, dict)


def test_format_json_contains_summary(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_json(sample_report)
    data = json.loads(output)
    assert "summary" in data
    assert "Detected 1 failure" in data["summary"]


def test_format_json_category_is_string(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_json(sample_report)
    data = json.loads(output)
    assert data["results"][0]["category"] == "dependency"


def test_format_json_has_metadata(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_json(sample_report)
    data = json.loads(output)
    assert "metadata" in data
    assert data["metadata"]["analyzer_version"] == "1.0.0"


def test_format_markdown_has_heading(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_markdown(sample_report)
    assert "# AI CI Failure Analyzer Report" in output


def test_format_markdown_contains_category(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_markdown(sample_report)
    assert "dependency" in output.lower()


def test_format_markdown_empty_report(formatter: ReportFormatter, empty_report: AnalysisReport) -> None:
    output = formatter.format_markdown(empty_report)
    assert "No failures detected" in output


def test_format_markdown_contains_fix(formatter: ReportFormatter, sample_report: AnalysisReport) -> None:
    output = formatter.format_markdown(sample_report)
    assert "pip install" in output
