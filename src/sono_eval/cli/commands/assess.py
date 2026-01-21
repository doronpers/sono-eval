import asyncio
import json
from typing import Optional, Tuple

import click
from rich.console import Console
from rich.table import Table

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.cli.formatters import (
    AssessmentFormatter,
    ErrorFormatter,
    ProgressFormatter,
)

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
                ErrorFormatter.format_file_error(file, "empty")
                raise click.Abort()
            final_content = content_str
        elif not content:
            ErrorFormatter.format_validation_error(
                field="content",
                message="Must provide either --file or --content",
                example="sono-eval assess run --candidate-id john_doe --file solution.py",
            )
            raise click.Abort()
        else:
            final_content = content
    except FileNotFoundError:
        ErrorFormatter.format_file_error(file, "not_found")
        raise click.Abort()
    except PermissionError:
        ErrorFormatter.format_file_error(file, "permission")
        raise click.Abort()
    except Exception as e:
        ErrorFormatter.format_error(
            error_type="File Error",
            message=f"Error reading file: {e}",
            suggestions=["Check file accessibility and format"],
            context={"file": file} if file else {},
        )
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

    # Run assessment with progress indicators
    try:
        engine = AssessmentEngine()

        if not quiet:
            # Show progress indicator
            progress = ProgressFormatter.create_assessment_progress()
            with progress:
                task = progress.add_task(
                    "Running assessment...",
                    total=len(path_list) + 1,
                )

                # Simulate stages for progress tracking
                progress.update(task, advance=0.5, description="Initializing assessment engine...")

                # Run the actual assessment
                result = asyncio.run(engine.assess(assessment_input))

                progress.update(
                    task,
                    advance=len(path_list) + 0.5,
                    description="Assessment complete!",
                )
        else:
            result = asyncio.run(engine.assess(assessment_input))

    except Exception as e:
        if verbose:
            import traceback

            ErrorFormatter.format_error(
                error_type="Assessment Error",
                message=f"Error running assessment: {e}",
                suggestions=[
                    "Verify the content is valid for assessment",
                    "Check that all required paths are valid",
                    "Try running with --verbose for more details",
                ],
                context={
                    "candidate_id": candidate_id,
                    "paths": ", ".join(p.value for p in path_list),
                    "traceback": traceback.format_exc(),
                },
            )
        else:
            ErrorFormatter.format_error(
                error_type="Assessment Error",
                message=f"Error running assessment: {e}",
                suggestions=[
                    "Verify the content is valid for assessment",
                    "Try running with --verbose for detailed error information",
                ],
            )
        raise click.Abort()

    # Display results using new formatter
    if not quiet:
        AssessmentFormatter.format_complete_result(result, verbose=verbose)

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
