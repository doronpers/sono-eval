import asyncio
import json
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType

console = Console()


@click.group()
def assess():
    """Assessment commands."""
    pass


@assess.command()
@click.option("--candidate-id", required=True, help="Candidate identifier")
@click.option("--file", type=click.Path(exists=True), help="Code file to assess")
@click.option("--content", help="Content to assess")
@click.option(
    "--type",
    default="code",
    help="Submission type (code, project, interview, portfolio, test)",
)
@click.option(
    "--paths",
    multiple=True,
    help="Paths to evaluate (technical, design, collaboration, problem_solving, communication)",
)
@click.option("--output", type=click.Path(), help="Output file for results (JSON format)")
@click.option("--quiet", is_flag=True, help="Quiet mode - minimal output")
@click.option("--verbose", is_flag=True, help="Verbose mode - detailed output")
def run(
    candidate_id: str,
    file: Optional[str],
    content: Optional[str],
    type: str,
    paths: Tuple[str, ...],
    output: Optional[str],
    quiet: bool,
    verbose: bool,
):
    """
    Run an assessment for a candidate.

    Examples:
        # Assess a code file with all paths
        sono-eval assess run --candidate-id john_doe --file solution.py

        # Assess specific paths only
        sono-eval assess run --candidate-id john_doe --file solution.py --paths technical design

        # Assess inline content
        sono-eval assess run --candidate-id john_doe \
            --content "def hello(): return 'world'" --paths technical

        # Save results to file
        sono-eval assess run --candidate-id john_doe --file solution.py --output results.json
    """
    if not quiet:
        console.print(f"[bold blue]Running assessment for candidate: {candidate_id}[/bold blue]")

    # Get content
    try:
        if file:
            if verbose:
                console.print(f"[dim]Reading file: {file}[/dim]")
            with open(file, "r", encoding="utf-8") as f:
                content_str = f.read()
            if not content_str.strip():
                console.print("[red]Error: File is empty[/red]")
                raise click.Abort()
            final_content = content_str
        elif not content:
            console.print("[red]Error: Must provide either --file or --content[/red]")
            console.print(
                "[yellow]Hint: Use --file path/to/file.py or --content 'your code here'[/yellow]"
            )
            raise click.Abort()
        else:
            final_content = content
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file}[/red]")
        raise click.Abort()
    except PermissionError:
        console.print(f"[red]Error: Permission denied reading file: {file}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        raise click.Abort()

    # Parse paths
    try:
        if paths:
            path_list = []
            for p in paths:
                try:
                    path_list.append(PathType[p.upper()])
                except KeyError:
                    console.print(
                        f"[yellow]Warning: Invalid path '{p}'. Valid paths: "
                        f"{', '.join(p.value for p in PathType)}[/yellow]"
                    )
            if not path_list:
                console.print("[red]Error: No valid paths specified[/red]")
                raise click.Abort()
        else:
            path_list = list(PathType)
            if not quiet:
                console.print(
                    f"[dim]No paths specified, evaluating all: "
                    f"{', '.join(p.value for p in path_list)}[/dim]"
                )
    except Exception as e:
        console.print(f"[red]Error parsing paths: {e}[/red]")
        raise click.Abort()

    # Create assessment input
    try:
        assessment_input = AssessmentInput(
            candidate_id=candidate_id,
            submission_type=type,
            content={"code": final_content},
            paths_to_evaluate=path_list,
        )
    except ValueError as e:
        console.print(f"[red]Validation error: {e}[/red]")
        raise click.Abort()

    # Run assessment
    if not quiet:
        console.print("[dim]Processing assessment...[/dim]")

    try:
        engine = AssessmentEngine()
        result = asyncio.run(engine.assess(assessment_input))
    except Exception as e:
        console.print(f"[red]Error running assessment: {e}[/red]")
        if verbose:
            import traceback

            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise click.Abort()

    # Display results
    if not quiet:
        console.print("\n[bold green]✓ Assessment Complete![/bold green]")
        console.print(f"Overall Score: [bold cyan]{result.overall_score:.2f}/100[/bold cyan]")
        console.print(f"Confidence: [cyan]{result.confidence:.2%}[/cyan]")
        if verbose:
            console.print(
                f"Processing Time: {result.processing_time_ms:.2f}ms"
                if result.processing_time_ms
                else ""
            )
        console.print(f"\n[bold]Summary:[/bold] {result.summary}")

        # Path scores table
        if result.path_scores:
            console.print("\n[bold]Path Scores:[/bold]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Path", style="cyan")
            table.add_column("Score", justify="right", style="green")
            table.add_column("Metrics", justify="right", style="dim")
            table.add_column("Strengths", justify="right", style="dim")

            for ps in result.path_scores:
                score_color = (
                    "green"
                    if ps.overall_score >= 75
                    else "yellow"
                    if ps.overall_score >= 60
                    else "red"
                )
                table.add_row(
                    ps.path.value.replace("_", " ").title(),
                    f"[{score_color}]{ps.overall_score:.1f}[/{score_color}]",
                    str(len(ps.metrics)),
                    str(len(ps.strengths)),
                )
            console.print(table)

        # Key findings
        if result.key_findings:
            console.print("\n[bold]Key Findings:[/bold]")
            for finding in result.key_findings:
                console.print(f"  • {finding}")

        # Recommendations
        if result.recommendations:
            console.print("\n[bold]Recommendations:[/bold]")
            for rec in result.recommendations:
                console.print(f"  • [yellow]{rec}[/yellow]")

        if verbose and result.micro_motives:
            console.print("\n[bold]Micro-Motives:[/bold]")
            for motive in result.micro_motives:
                console.print(f"  • {motive.motive_type.value}: {motive.strength:.2f} strength")

    # Save to file if requested
    if output:
        try:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(result.model_dump(mode="json"), f, indent=2, default=str)
            if not quiet:
                console.print(f"\n[green]✓ Results saved to {output}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving results: {e}[/red]")

    if quiet:
        # In quiet mode, just print the score
        console.print(f"{result.overall_score:.2f}")
