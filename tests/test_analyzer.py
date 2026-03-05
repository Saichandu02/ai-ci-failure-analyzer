"""Tests for FailureAnalyzer."""

from __future__ import annotations

import re

from ai_ci_analyzer.analyzer import FailureAnalyzer
from ai_ci_analyzer.models import AnalysisReport, FailureCategory


def test_analyze_returns_report(analyzer: FailureAnalyzer, sample_dependency_log: str) -> None:
    report = analyzer.analyze(sample_dependency_log)
    assert isinstance(report, AnalysisReport)


def test_analyze_detects_dependency_failure(analyzer: FailureAnalyzer, sample_dependency_log: str) -> None:
    report = analyzer.analyze(sample_dependency_log)
    categories = [r.category for r in report.results]
    assert FailureCategory.DEPENDENCY in categories


def test_analyze_detects_test_failure(analyzer: FailureAnalyzer, sample_test_failure_log: str) -> None:
    report = analyzer.analyze(sample_test_failure_log)
    categories = [r.category for r in report.results]
    assert FailureCategory.TEST in categories


def test_analyze_detects_timeout(analyzer: FailureAnalyzer, sample_timeout_log: str) -> None:
    report = analyzer.analyze(sample_timeout_log)
    categories = [r.category for r in report.results]
    assert FailureCategory.TIMEOUT in categories


def test_analyze_detects_network_failure(analyzer: FailureAnalyzer, sample_network_log: str) -> None:
    report = analyzer.analyze(sample_network_log)
    categories = [r.category for r in report.results]
    assert FailureCategory.NETWORK in categories


def test_analyze_clean_log_no_failures(analyzer: FailureAnalyzer, sample_clean_log: str) -> None:
    report = analyzer.analyze(sample_clean_log)
    assert report.results == []
    assert "No failures detected" in report.summary


def test_analyze_report_has_metadata(analyzer: FailureAnalyzer, sample_dependency_log: str) -> None:
    report = analyzer.analyze(sample_dependency_log)
    assert "analyzer_version" in report.metadata
    assert "patterns_checked" in report.metadata
    assert "timestamp" in report.metadata


def test_analyze_results_sorted_by_confidence(analyzer: FailureAnalyzer) -> None:
    log = "ModuleNotFoundError: No module named 'foo'\n" * 5 + "FAILED tests/test_bar.py::test_x - AssertionError\n"
    report = analyzer.analyze(log)
    if len(report.results) > 1:
        scores = [r.confidence_score for r in report.results]
        assert scores == sorted(scores, reverse=True)


def test_analyze_confidence_score_range(analyzer: FailureAnalyzer, sample_dependency_log: str) -> None:
    report = analyzer.analyze(sample_dependency_log)
    for result in report.results:
        assert 0.0 <= result.confidence_score <= 1.0


def test_analyze_summary_mentions_categories(analyzer: FailureAnalyzer, sample_dependency_log: str) -> None:
    report = analyzer.analyze(sample_dependency_log)
    assert "dependency" in report.summary


def test_analyze_total_lines_count(analyzer: FailureAnalyzer) -> None:
    log = "line1\nline2\nline3\n"
    report = analyzer.analyze(log)
    assert report.total_lines == 3


def test_analyze_error_count(analyzer: FailureAnalyzer) -> None:
    log = "ERROR: something failed\nWARNING: something deprecated\ninfo line\n"
    report = analyzer.analyze(log)
    assert report.error_count == 2


def test_analyze_custom_patterns(sample_dependency_log: str) -> None:
    custom_patterns = [
        {
            "pattern": re.compile(r"custom error pattern", re.IGNORECASE),
            "category": FailureCategory.UNKNOWN,
            "description": "Custom pattern",
            "suggested_fix": "Custom fix",
        }
    ]
    analyzer = FailureAnalyzer(patterns=custom_patterns)
    report = analyzer.analyze(sample_dependency_log)
    assert report.results == []


def test_analyze_empty_log(analyzer: FailureAnalyzer) -> None:
    report = analyzer.analyze("")
    assert report.results == []
    assert report.total_lines == 0


def test_one_result_per_category(analyzer: FailureAnalyzer) -> None:
    log = (
        "ModuleNotFoundError: No module named 'foo'\n" + "Cannot find module 'bar'\n" + "npm ERR! missing dependency\n"
    )
    report = analyzer.analyze(log)
    categories = [r.category for r in report.results]
    assert len(categories) == len(set(categories)), "Duplicate categories found"
