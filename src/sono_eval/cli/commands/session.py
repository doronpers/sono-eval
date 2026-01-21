"""Session management commands for Sono-Eval CLI."""

import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.table import Table

from sono_eval.cli.session_manager import end_current_session, get_session
from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


def format_session_report_as_markdown(report_data: dict) -> str:
    """Format session report as markdown (helper function)."""
    lines = [
        f"# Session Report: {report_data['session_id'][:8]}",
        "",
        f"**Date:** {report_data['date']}",
        f"**Duration:** {report_data['duration']}",
        f"**Candidate ID:** {report_data['candidate_id'] or 'N/A'}",
        f"**Total Assessments:** {report_data['total_assessments']}",
        f"**Average Score:** {report_data['average_score']}/100",
        "",
        "## Key Insights",
        "",
    ]

    if report_data["key_insights"]:
        for insight in report_data["key_insights"]:
            lines.append(f"- {insight}")
    else:
        lines.append("*No insights available*")

    lines.extend(
        [
            "",
            "## Recommendations",
            "",
        ]
    )

    if report_data["recommendations"]:
        for rec in report_data["recommendations"]:
            lines.append(f"- {rec}")
    else:
        lines.append("*No recommendations available*")

    lines.extend(
        [
            "",
            "## Strengths",
            "",
        ]
    )

    if report_data["strengths"]:
        for strength in report_data["strengths"]:
            lines.append(f"- {strength}")
    else:
        lines.append("*No strengths identified*")

    lines.extend(
        [
            "",
            "## Areas for Improvement",
            "",
        ]
    )

    if report_data["areas_for_improvement"]:
        for area in report_data["areas_for_improvement"]:
            lines.append(f"- {area}")
    else:
        lines.append("*No areas identified*")

    if report_data.get("notes"):
        lines.extend(
            [
                "",
                "## Session Notes",
                "",
            ]
        )
        for note in report_data["notes"]:
            lines.append(f"- {note}")

    return "\n".join(lines)


@click.group()
def session():
    """Session management commands."""
    pass


@session.command()
@click.option("--output", type=click.Path(), help="Output file for report (JSON or Markdown)")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["json", "markdown"]),
    default="markdown",
)
def report(output: Optional[str], output_format: str):
    """
    Generate a session report for the current session.

    Examples:
        # Display session report
        sono-eval session report

        # Save as Markdown
        sono-eval session report --output session_report.md

        # Save as JSON
        sono-eval session report --format json --output session_report.json
    """
    try:
        session = get_session()
        report_data = session.generate_session_report()

        if output_format == "json":
            report_content = json.dumps(report_data, indent=2, default=str)
        else:
            # Format as Markdown using helper function
            report_content = format_session_report_as_markdown(report_data)

        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(report_content)
            console.print(f"[green]✓ Session report saved to {output}[/green]")
        else:
            if output_format == "markdown":
                console.print(Markdown(report_content))
            else:
                console.print(report_content)

    except Exception as e:
        console.print(f"[red]Error generating session report: {e}[/red]")
        raise click.Abort()


@session.command()
def end():
    """
    End the current session and generate a report.

    Examples:
        # End current session
        sono-eval session end
    """
    try:
        session = get_session()
        report_data = session.generate_session_report()

        console.print("\n[bold cyan]Session Summary[/bold cyan]")
        console.print(f"Duration: {report_data['duration']}")
        console.print(f"Assessments: {report_data['total_assessments']}")
        console.print(f"Average Score: {report_data['average_score']}/100")

        if Confirm.ask("\n[cyan]Generate session report?[/cyan]", default=True):
            report_data = session.generate_session_report()
            lines = [
                f"# Session Report: {report_data['session_id'][:8]}",
                "",
                f"**Date:** {report_data['date']}",
                f"**Duration:** {report_data['duration']}",
                f"**Total Assessments:** {report_data['total_assessments']}",
                f"**Average Score:** {report_data['average_score']}/100",
                "",
            ]
            console.print(Markdown("\n".join(lines)))

        end_current_session()
        console.print("\n[green]✓ Session ended successfully[/green]")

    except Exception as e:
        console.print(f"[red]Error ending session: {e}[/red]")
        raise click.Abort()


@session.command()
def list():
    """
    List all previous sessions.

    Examples:
        # List all sessions
        sono-eval session list
    """
    try:
        config = get_config()
        sessions_dir = Path(config.memu_storage_path).parent / "sessions"

        if not sessions_dir.exists():
            console.print("[yellow]No sessions found[/yellow]")
            return

        sessions = []
        for session_file in sessions_dir.glob("*.json"):
            try:
                with open(session_file, "r") as f:
                    data = json.load(f)
                    sessions.append(data)
            except Exception as e:
                logger.debug(f"Failed to load session {session_file}: {e}")
                continue

        if not sessions:
            console.print("[yellow]No sessions found[/yellow]")
            return

        # Sort by start time (newest first)
        sessions.sort(key=lambda x: x.get("start_time", ""), reverse=True)

        console.print(f"\n[bold cyan]Previous Sessions ({len(sessions)})[/bold cyan]\n")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Session ID", style="dim")
        table.add_column("Date", style="cyan")
        table.add_column("Duration", justify="right")
        table.add_column("Assessments", justify="right")
        table.add_column("Candidate ID", style="dim")

        for s in sessions[:20]:  # Show last 20
            start_time = s.get("start_time", "")
            date_str = start_time[:10] if start_time else "N/A"
            duration = s.get("duration_seconds", 0)
            duration_str = f"{int(duration // 60)}m {int(duration % 60)}s"

            table.add_row(
                s.get("session_id", "")[:8],
                date_str,
                duration_str,
                str(len(s.get("assessments", []))),
                s.get("candidate_id", "N/A") or "N/A",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[red]Error listing sessions: {e}[/red]")
        raise click.Abort()
