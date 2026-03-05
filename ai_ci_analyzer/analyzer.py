"""Core failure analyzer for CI logs."""

from __future__ import annotations

import re
from datetime import UTC, datetime
from typing import Any

from ai_ci_analyzer import __version__
from ai_ci_analyzer.models import AnalysisReport, AnalysisResult, CILogEntry, FailureCategory
from ai_ci_analyzer.parser import LogParser
from ai_ci_analyzer.patterns import FAILURE_PATTERNS


class FailureAnalyzer:
    """Analyzes CI logs for failure patterns and generates analysis reports."""

    def __init__(self, patterns: list[dict] | None = None) -> None:
        """Initialize the analyzer with optional custom patterns."""
        self._patterns = patterns if patterns is not None else FAILURE_PATTERNS
        self._parser = LogParser()

    def analyze(self, log_text: str) -> AnalysisReport:
        """Analyze CI log text and return a full analysis report."""
        entries = self._parser.parse(log_text)
        results = self._match_patterns(log_text, entries)
        results.sort(key=lambda r: r.confidence_score, reverse=True)
        error_entries = self._parser.extract_error_sections(entries)
        metadata: dict[str, Any] = {
            "analyzer_version": __version__,
            "patterns_checked": len(self._patterns),
            "timestamp": datetime.now(tz=UTC).isoformat(),
        }
        summary = self._generate_summary(results)
        return AnalysisReport(
            summary=summary,
            results=results,
            metadata=metadata,
            total_lines=len(entries),
            error_count=len(error_entries),
        )

    def _match_patterns(self, text: str, entries: list[CILogEntry]) -> list[AnalysisResult]:
        """Match failure patterns against log text."""
        results: list[AnalysisResult] = []
        seen_categories: dict[FailureCategory, list[AnalysisResult]] = {}

        for pattern_def in self._patterns:
            compiled: re.Pattern[str] = pattern_def["pattern"]
            matches = compiled.findall(text)
            if not matches:
                continue

            category: FailureCategory = pattern_def["category"]
            relevant: list[str] = []
            for entry in entries:
                if compiled.search(entry.message):
                    relevant.append(entry.message)

            match_count = len(matches)
            confidence = self._calculate_confidence([match_count])

            result = AnalysisResult(
                category=category,
                root_cause=pattern_def["description"],
                confidence_score=confidence,
                suggested_fix=pattern_def["suggested_fix"],
                relevant_lines=relevant[:5],
            )
            if category not in seen_categories:
                seen_categories[category] = []
            seen_categories[category].append(result)

        # Keep the highest-confidence result per category
        for category_results in seen_categories.values():
            best = max(category_results, key=lambda r: r.confidence_score)
            results.append(best)

        return results

    def _calculate_confidence(self, matches: list) -> float:
        """Calculate a confidence score based on the number of matches."""
        if not matches:
            return 0.0
        count = matches[0] if isinstance(matches[0], int) else len(matches)
        if count >= 5:
            return 1.0
        return min(0.5 + (count - 1) * 0.1, 1.0)

    def _generate_summary(self, results: list[AnalysisResult]) -> str:
        """Generate a human-readable summary from analysis results."""
        if not results:
            return "No failures detected in the CI log."
        categories = [r.category.value for r in results]
        unique = list(dict.fromkeys(categories))
        category_str = ", ".join(unique)
        return f"Detected {len(results)} failure(s) in categories: {category_str}."
