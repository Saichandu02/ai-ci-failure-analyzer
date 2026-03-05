"""Tests for failure patterns."""

from __future__ import annotations

from ai_ci_analyzer.models import FailureCategory
from ai_ci_analyzer.patterns import FAILURE_PATTERNS


def test_patterns_list_not_empty() -> None:
    assert len(FAILURE_PATTERNS) > 0


def test_each_pattern_has_required_keys() -> None:
    required_keys = {"pattern", "category", "description", "suggested_fix"}
    for p in FAILURE_PATTERNS:
        assert required_keys.issubset(p.keys()), f"Pattern missing keys: {p}"


def test_each_pattern_category_is_valid() -> None:
    valid_categories = set(FailureCategory)
    for p in FAILURE_PATTERNS:
        assert p["category"] in valid_categories


def test_dependency_pattern_matches() -> None:
    dep_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.DEPENDENCY]
    assert len(dep_patterns) > 0
    sample = "ModuleNotFoundError: No module named 'requests'"
    matched = any(p["pattern"].search(sample) for p in dep_patterns)
    assert matched


def test_test_failure_pattern_matches() -> None:
    test_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.TEST]
    assert len(test_patterns) > 0
    sample = "FAILED tests/test_foo.py::test_bar - AssertionError"
    matched = any(p["pattern"].search(sample) for p in test_patterns)
    assert matched


def test_timeout_pattern_matches() -> None:
    timeout_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.TIMEOUT]
    assert len(timeout_patterns) > 0
    sample = "ERROR: Job timed out after 60 minutes"
    matched = any(p["pattern"].search(sample) for p in timeout_patterns)
    assert matched


def test_network_pattern_matches() -> None:
    net_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.NETWORK]
    assert len(net_patterns) > 0
    sample = "Connection refused to host example.com"
    matched = any(p["pattern"].search(sample) for p in net_patterns)
    assert matched


def test_permission_pattern_matches() -> None:
    perm_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.PERMISSION]
    assert len(perm_patterns) > 0
    sample = "Permission denied: /etc/secret"
    matched = any(p["pattern"].search(sample) for p in perm_patterns)
    assert matched


def test_resource_pattern_matches() -> None:
    res_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.RESOURCE]
    assert len(res_patterns) > 0
    sample = "MemoryError: unable to allocate array"
    matched = any(p["pattern"].search(sample) for p in res_patterns)
    assert matched


def test_syntax_pattern_matches() -> None:
    syntax_patterns = [p for p in FAILURE_PATTERNS if p["category"] == FailureCategory.SYNTAX]
    assert len(syntax_patterns) > 0
    sample = "SyntaxError: invalid syntax"
    matched = any(p["pattern"].search(sample) for p in syntax_patterns)
    assert matched
