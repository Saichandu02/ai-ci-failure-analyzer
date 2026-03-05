"""Report formatters for CI analysis results."""

from __future__ import annotations

import dataclasses
import json

from ai_ci_analyzer.models import AnalysisReport, FailureCategory


class ReportFormatter:
    """Formats AnalysisReport objects into various output formats."""

    def format_text(self, report: AnalysisReport) -> str:
        """Format a report as human-readable plain text."""
        lines: list[str] = [
            "=" * 60,
            "AI CI FAILURE ANALYZER REPORT",
            "=" * 60,
            f"Summary: {report.summary}",
            f"Total lines parsed: {report.total_lines}",
            f"Error entries: {report.error_count}",
            "",
        ]
        if not report.results:
            lines.append("No failures detected.")
        else:
            for i, result in enumerate(report.results, start=1):
                lines.append(f"--- Failure #{i} ---")
                lines.append(f"Category:       {result.category.value}")
                lines.append(f"Root Cause:     {result.root_cause}")
                lines.append(f"Confidence:     {result.confidence_score:.0%}")
                lines.append(f"Suggested Fix:  {result.suggested_fix}")
                if result.relevant_lines:
                    lines.append("Relevant Lines:")
                    for line in result.relevant_lines:
                        lines.append(f"  {line}")
                lines.append("")
        lines.append("=" * 60)
        meta = report.metadata
        lines.append(f"Analyzer version: {meta.get('analyzer_version', 'N/A')}")
        lines.append(f"Patterns checked: {meta.get('patterns_checked', 'N/A')}")
        lines.append(f"Timestamp:        {meta.get('timestamp', 'N/A')}")
        lines.append("=" * 60)
        return "\n".join(lines)

    def format_json(self, report: AnalysisReport) -> str:
        """Format a report as JSON."""
        raw = dataclasses.asdict(report)
        self._convert_enums(raw)
        return json.dumps(raw, indent=2, default=str)

    def format_markdown(self, report: AnalysisReport) -> str:
        """Format a report as Markdown suitable for PR comments."""
        lines: list[str] = [
            "# AI CI Failure Analyzer Report",
            "",
            f"**Summary:** {report.summary}",
            f"- Total lines parsed: `{report.total_lines}`",
            f"- Error entries found: `{report.error_count}`",
            "",
        ]
        if not report.results:
            lines.append("✅ **No failures detected.**")
        else:
            lines.append("## Detected Failures")
            lines.append("")
            for i, result in enumerate(report.results, start=1):
                lines.append(f"### Failure #{i}: {result.category.value.capitalize()}")
                lines.append("")
                lines.append(f"- **Root Cause:** {result.root_cause}")
                lines.append(f"- **Confidence:** {result.confidence_score:.0%}")
                lines.append(f"- **Suggested Fix:** {result.suggested_fix}")
                if result.relevant_lines:
                    lines.append("- **Relevant Lines:**")
                    lines.append("  ```")
                    for line in result.relevant_lines:
                        lines.append(f"  {line}")
                    lines.append("  ```")
                lines.append("")
        lines.append("---")
        meta = report.metadata
        lines.append(
            f"*Analyzer version: {meta.get('analyzer_version', 'N/A')} | "
            f"Patterns checked: {meta.get('patterns_checked', 'N/A')} | "
            f"Timestamp: {meta.get('timestamp', 'N/A')}*"
        )
        return "\n".join(lines)

    def _convert_enums(self, obj: object) -> None:
        """Recursively convert FailureCategory enum values to strings in a dict."""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, FailureCategory):
                    obj[key] = value.value
                elif isinstance(value, (dict, list)):
                    self._convert_enums(value)
        elif isinstance(obj, list):
            for item in obj:
                self._convert_enums(item)
