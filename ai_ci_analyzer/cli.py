"""Command-line interface for the AI CI Failure Analyzer."""

from __future__ import annotations

import sys

import click

from ai_ci_analyzer.analyzer import FailureAnalyzer
from ai_ci_analyzer.reporter import ReportFormatter


@click.command()
@click.argument("log_file", required=False, type=click.Path(exists=True))
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["text", "json", "markdown"]),
    default="text",
    help="Output format.",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose output.")
@click.option("--stdin", is_flag=True, help="Read log from stdin.")
def main(
    log_file: str | None,
    output_format: str,
    verbose: bool,
    stdin: bool,
) -> None:
    """Analyze CI log files for failure patterns.

    Provide a LOG_FILE path or use --stdin to read from standard input.
    """
    try:
        if stdin:
            log_text = sys.stdin.read()
        elif log_file:
            with open(log_file) as fh:
                log_text = fh.read()
        else:
            click.echo("Error: provide a log file or use --stdin.", err=True)
            sys.exit(2)

        analyzer = FailureAnalyzer()
        formatter = ReportFormatter()
        report = analyzer.analyze(log_text)

        if verbose:
            click.echo(
                f"Parsed {report.total_lines} lines, found {report.error_count} error entries.",
                err=True,
            )

        if output_format == "json":
            output = formatter.format_json(report)
        elif output_format == "markdown":
            output = formatter.format_markdown(report)
        else:
            output = formatter.format_text(report)

        click.echo(output)
        sys.exit(1 if report.results else 0)
    except Exception as exc:  # noqa: BLE001
        click.echo(f"Error: {exc}", err=True)
        sys.exit(2)
