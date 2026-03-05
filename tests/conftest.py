"""Pytest fixtures for AI CI Failure Analyzer tests."""

from __future__ import annotations

import pytest

from ai_ci_analyzer.analyzer import FailureAnalyzer
from ai_ci_analyzer.parser import LogParser
from ai_ci_analyzer.reporter import ReportFormatter


@pytest.fixture
def analyzer() -> FailureAnalyzer:
    return FailureAnalyzer()


@pytest.fixture
def parser() -> LogParser:
    return LogParser()


@pytest.fixture
def formatter() -> ReportFormatter:
    return ReportFormatter()


@pytest.fixture
def sample_dependency_log() -> str:
    return (
        "Step 1/3: Installing dependencies\n"
        "ERROR: ModuleNotFoundError: No module named 'requests'\n"
        "pip install failed\n"
    )


@pytest.fixture
def sample_test_failure_log() -> str:
    return (
        "collected 5 items\n"
        "FAILED tests/test_foo.py::test_bar - AssertionError: assert 1 == 2\n"
        "1 failed, 4 passed\n"
    )


@pytest.fixture
def sample_timeout_log() -> str:
    return "ERROR: Job timed out after 60 minutes\n"


@pytest.fixture
def sample_network_log() -> str:
    return "curl: (7) Failed to connect to example.com: Connection refused\n"


@pytest.fixture
def sample_clean_log() -> str:
    return "Step 1/3: Checkout\n" "Step 2/3: Install deps\n" "Step 3/3: Run tests\n" "All tests passed!\n"
