import json
from datetime import datetime, timezone
from typing import Optional

import click
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

from sono_eval.memory.memu import MemUStorage

console = Console()


@click.group()
def candidate():
    """Candidate management commands."""
    pass


@candidate.command()
@click.option(
    "--id",
    "candidate_id",
    required=True,
    help="Candidate ID (alphanumeric, dashes, underscores only)",
)
@click.option("--data", help="Initial data (JSON string)")
@click.option("--quiet", is_flag=True, help="Quiet mode - minimal output")
def create(candidate_id: str, data: Optional[str], quiet: bool):
    """
    Create a new candidate in memory storage.

    Examples:
        # Create a candidate
        sono-eval candidate create --id john_doe

        # Create with initial data
        sono-eval candidate create --id john_doe \
            --data '{"email": "john@example.com"}'
    """
    try:
        storage = MemUStorage()

        initial_data = None
        if data:
            try:
                initial_data = json.loads(data)
            except json.JSONDecodeError as e:
                console.print(f"[red]Error: Invalid JSON in --data: {e}[/red]")
                raise click.Abort()

        # Check if candidate already exists
        existing = storage.get_candidate_memory(candidate_id)
        if existing:
            console.print(
                f"[yellow]Warning: Candidate '{candidate_id}' already exists[/yellow]"
            )
            if not click.confirm("Do you want to continue anyway?"):
                raise click.Abort()

        memory = storage.create_candidate_memory(candidate_id, initial_data)
        if not quiet:
            console.print(f"[green]✓ Created candidate: {memory.candidate_id}[/green]")
            console.print(f"[dim]Created: {memory.last_updated}[/dim]")
    except ValueError as e:
        console.print(f"[red]Validation error: {e}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error creating candidate: {e}[/red]")
        raise click.Abort()


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
@click.option("--verbose", is_flag=True, help="Show detailed information")
def show(candidate_id: str, verbose: bool):
    """
    Show candidate information and memory structure.

    Examples:
        # Show basic info
        sono-eval candidate show --id john_doe

        # Show detailed info
        sono-eval candidate show --id john_doe --verbose
    """
    try:
        storage = MemUStorage()
        memory = storage.get_candidate_memory(candidate_id)

        if not memory:
            console.print(f"[red]Error: Candidate not found: {candidate_id}[/red]")
            console.print(
                "[yellow]Hint: Use 'sono-eval candidate create' to create a new candidate[/yellow]"
            )
            raise click.Abort()

        console.print(f"\n[bold cyan]Candidate: {memory.candidate_id}[/bold cyan]")
        console.print(f"[dim]Last Updated:[/dim] {memory.last_updated}")
        console.print(f"[dim]Memory Nodes:[/dim] {len(memory.nodes)}")
        console.print(f"[dim]Version:[/dim] {memory.version}")

        # Show root data
        if memory.root_node.data:
            console.print("\n[bold]Initial Data:[/bold]")
            console.print(json.dumps(memory.root_node.data, indent=2))

        if verbose:
            console.print("\n[bold]Memory Structure:[/bold]")
            console.print(f"Root Node ID: {memory.root_node.node_id}")
            if memory.root_node.children:
                console.print(f"Child Nodes: {', '.join(memory.root_node.children)}")
    except Exception as e:
        console.print(f"[red]Error retrieving candidate: {e}[/red]")
        raise click.Abort()


@candidate.command()
@click.option("--quiet", is_flag=True, help="Quiet mode - just list IDs")
def list(quiet: bool):
    """
    List all candidates in memory storage.

    Examples:
        # List all candidates
        sono-eval candidate list

        # Quiet mode (just IDs)
        sono-eval candidate list --quiet
    """
    try:
        storage = MemUStorage()
        candidates = storage.list_candidates()

        if not candidates:
            console.print("[yellow]No candidates found[/yellow]")
            console.print(
                "[dim]Use 'sono-eval candidate create' to create a candidate[/dim]"
            )
            return

        if quiet:
            for candidate_id in candidates:
                console.print(candidate_id)
        else:
            console.print(f"\n[bold cyan]Candidates ({len(candidates)}):[/bold cyan]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Candidate ID", style="cyan")

            for candidate_id in candidates:
                memory = storage.get_candidate_memory(candidate_id)
                if memory:
                    table.add_row(
                        candidate_id,
                    )
            console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing candidates: {e}[/red]")
        raise click.Abort()


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
@click.confirmation_option(prompt="Are you sure you want to delete this candidate?")
def delete(candidate_id: str):
    """Delete a candidate."""
    storage = MemUStorage()
    success = storage.delete_candidate_memory(candidate_id)

    if success:
        console.print(f"[green]Deleted candidate: {candidate_id}[/green]")
    else:
        console.print(f"[red]Candidate not found: {candidate_id}[/red]")


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
@click.option("--limit", default=10, help="Maximum assessments to show")
@click.option(
    "--format", "output_format", type=click.Choice(["table", "json"]), default="table"
)
def history(candidate_id: str, limit: int, output_format: str):
    """
    Show assessment history for a candidate.

    Examples:
        # View last 10 assessments
        sono-eval candidate history --id john_doe

        # View as JSON
        sono-eval candidate history --id john_doe --format json --limit 5
    """
    try:
        storage = MemUStorage()
        memory = storage.get_candidate_memory(candidate_id)

        if not memory:
            console.print(f"[red]Error: Candidate not found: {candidate_id}[/red]")
            raise click.Abort()

        # Collect assessments
        assessments = []
        for node in memory.nodes.values():
            if node.metadata.get("type") == "assessment":
                result_data = node.data.get("assessment_result")
                if result_data:
                    assessments.append(
                        {
                            "assessment_id": result_data.get("assessment_id"),
                            "timestamp": result_data.get("timestamp"),
                            "overall_score": result_data.get("overall_score"),
                            "confidence": result_data.get("confidence"),
                            "dominant_path": result_data.get("dominant_path"),
                            "paths_evaluated": len(result_data.get("path_scores", [])),
                        }
                    )

        # Sort by timestamp (newest first)
        assessments.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
        assessments = assessments[:limit]

        if not assessments:
            console.print(f"[yellow]No assessments found for {candidate_id}[/yellow]")
            return

        if output_format == "json":
            console.print(json.dumps(assessments, indent=2, default=str))
        else:
            console.print(
                f"\n[bold cyan]Assessment History for {candidate_id}[/bold cyan]"
            )
            console.print(
                f"[dim]Showing {len(assessments)} of {len(assessments)} assessments[/dim]\n"
            )

            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Date", style="dim")
            table.add_column("Score", justify="right")
            table.add_column("Confidence", justify="right")
            table.add_column("Dominant Path")
            table.add_column("Paths", justify="center")
            table.add_column("ID", style="dim")

            for a in assessments:
                score = a.get("overall_score", 0)
                score_color = (
                    "green" if score >= 75 else "yellow" if score >= 60 else "red"
                )

                # Format timestamp
                ts = a.get("timestamp", "")
                if ts:
                    try:
                        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                        ts = dt.strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        pass  # nosec B110

                table.add_row(
                    ts[:16] if ts else "N/A",
                    f"[{score_color}]{score:.1f}[/{score_color}]",
                    f"{a.get('confidence', 0) * 100:.0f}%",
                    a.get("dominant_path", "N/A"),
                    str(a.get("paths_evaluated", 0)),
                    a.get("assessment_id", "")[:15] + "...",
                )

            console.print(table)

            # Show trend
            if len(assessments) >= 2:
                scores = [a.get("overall_score", 0) for a in assessments]
                recent_avg = sum(scores[:3]) / min(3, len(scores))
                older_avg = (
                    sum(scores[3:]) / max(1, len(scores) - 3)
                    if len(scores) > 3
                    else recent_avg
                )

                if recent_avg > older_avg + 5:
                    console.print("\n[green]📈 Trend: Improving[/green]")
                elif recent_avg < older_avg - 5:
                    console.print("\n[red]📉 Trend: Declining[/red]")
                else:
                    console.print("\n[yellow]➡️ Trend: Stable[/yellow]")

    except Exception as e:
        console.print(f"[red]Error retrieving history: {e}[/red]")
        raise click.Abort()


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
@click.option("--output", type=click.Path(), help="Output file for report")
def report(candidate_id: str, output: Optional[str]):
    """
    Generate a comprehensive report for a candidate.

    Examples:
        # Generate and display report
        sono-eval candidate report --id john_doe

        # Save to file
        sono-eval candidate report --id john_doe --output report.md
    """
    try:
        storage = MemUStorage()
        memory = storage.get_candidate_memory(candidate_id)

        if not memory:
            console.print(f"[red]Error: Candidate not found: {candidate_id}[/red]")
            raise click.Abort()

        # Collect all assessments
        assessments = []
        for node in memory.nodes.values():
            if node.metadata.get("type") == "assessment":
                result_data = node.data.get("assessment_result")
                if result_data:
                    assessments.append(result_data)

        if not assessments:
            console.print(f"[yellow]No assessments found for {candidate_id}[/yellow]")
            return

        # Sort by timestamp
        assessments.sort(key=lambda x: x.get("timestamp", ""))

        # Generate report
        report_lines = [
            f"# Assessment Report: {candidate_id}",
            "",
            f"**Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
            f"**Total Assessments:** {len(assessments)}",
            "",
            "## Overview",
            "",
        ]

        # Calculate statistics
        scores = [a.get("overall_score", 0) for a in assessments]
        avg_score = sum(scores) / len(scores)
        best_score = max(scores)
        latest_score = scores[-1] if scores else 0

        report_lines.extend(
            [
                "| Metric | Value |",
                "|--------|-------|",
                f"| Average Score | {avg_score:.1f} |",
                f"| Best Score | {best_score:.1f} |",
                f"| Latest Score | {latest_score:.1f} |",
                f"| Total Assessments | {len(assessments)} |",
                "",
                "## Assessment History",
                "",
            ]
        )

        for i, a in enumerate(assessments[-5:], 1):  # Last 5
            report_lines.extend(
                [
                    f"### Assessment {i}",
                    "",
                    f"- **ID:** {a.get('assessment_id', 'N/A')}",
                    f"- **Score:** {a.get('overall_score', 0):.1f}/100",
                    f"- **Confidence:** {a.get('confidence', 0) * 100:.0f}%",
                    f"- **Summary:** {a.get('summary', 'N/A')}",
                    "",
                ]
            )

        report_content = "\n".join(report_lines)

        if output:
            with open(output, "w") as f:
                f.write(report_content)
            console.print(f"[green]✓ Report saved to {output}[/green]")
        else:
            console.print(Markdown(report_content))

    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")
        raise click.Abort()
