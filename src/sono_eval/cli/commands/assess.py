import asyncio
import json
from typing import Optional, Tuple

import click
from rich.console import Console

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.cli.formatters import AssessmentFormatter, ErrorFormatter, ProgressFormatter
from sono_eval.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


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

        # Show personalized greeting if available
        try:
            from sono_eval.cli.personalization import PersonalizationEngine

            personalizer = PersonalizationEngine(candidate_id)
            greeting = personalizer.get_greeting_message()
            console.print(f"[dim]{greeting}[/dim]\n")

            # Show contextual insights
            insights = personalizer.get_contextual_insights()
            if insights:
                console.print("[bold cyan]Insights from your history:[/bold cyan]")
                for insight in insights[:2]:
                    console.print(f"  • {insight}")
                console.print()
        except Exception as e:
            logger.debug(f"Personalization greeting failed: {e}")

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

        # Personalized recommendations
        try:
            from sono_eval.cli.personalization import PersonalizationEngine

            personalizer = PersonalizationEngine(candidate_id)
            personalized_recs = personalizer.get_personalized_recommendations()
            if personalized_recs:
                console.print("\n[bold cyan]Personalized Recommendations:[/bold cyan]")
                for rec in personalized_recs[:3]:
                    console.print(f"  • [cyan]{rec}[/cyan]")
        except Exception as e:
            logger.debug(f"Personalized recommendations failed: {e}")

    # Save assessment to memory for cross-session persistence
    try:
        from sono_eval.memory.memu import MemUStorage

        storage = MemUStorage()

        # Ensure candidate memory exists
        memory = storage.get_candidate_memory(candidate_id)
        if not memory:
            memory = storage.create_candidate_memory(candidate_id)

        # Add assessment as a memory node
        root_id = memory.root_node.node_id
        storage.add_memory_node(
            candidate_id=candidate_id,
            parent_id=root_id,
            data={"assessment_result": result.model_dump(mode="json")},
            metadata={"type": "assessment", "assessment_id": result.assessment_id},
        )
        logger.debug(f"Saved assessment {result.assessment_id} to memory")
    except Exception as e:
        logger.warning(f"Failed to save assessment to memory: {e}")

    # Track assessment in session
    try:
        from sono_eval.cli.session_manager import get_session

        session = get_session(candidate_id)
        session.add_assessment(result.model_dump(mode="json"))
    except Exception as e:
        logger.debug(f"Failed to track assessment in session: {e}")

    # Save to file if requested
    if output:
        try:
            with open(output, "w", encoding="utf-8") as f:
                json.dump(result.model_dump(mode="json"), f, indent=2, default=str)
            if not quiet:
                console.print(f"\n[green]✓ Results saved to {output}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving results: {e}[/red]")
    elif not quiet:
        # Offer to save if not already saved
        try:
            from rich.prompt import Confirm

            if Confirm.ask(
                "\n[cyan]Would you like to save the raw results to a file?[/cyan]",
                default=False,
            ):
                default_output = f"assessment_{result.assessment_id}.json"
                from rich.prompt import Prompt

                save_path = Prompt.ask("Output file path", default=default_output)
                try:
                    with open(save_path, "w", encoding="utf-8") as f:
                        json.dump(result.model_dump(mode="json"), f, indent=2, default=str)
                    console.print(f"[green]✓ Results saved to {save_path}[/green]")
                except Exception as e:
                    console.print(f"[red]Error saving results: {e}[/red]")
        except ImportError:
            pass  # rich.prompt not available, skip

    if quiet:
        # In quiet mode, just print the score
        console.print(f"{result.overall_score:.2f}")
    else:
        # Auto-generate session report if this is the last assessment in session
        try:
            from sono_eval.cli.session_manager import get_session

            session = get_session(candidate_id)
            if len(session.assessments) >= 1:  # After first assessment
                # Offer to generate session report
                try:
                    from rich.prompt import Confirm

                    if Confirm.ask("\n[cyan]Generate session report?[/cyan]", default=False):
                        report_data = session.generate_session_report()
                        from sono_eval.cli.commands.session import format_session_report_as_markdown

                        report_md = format_session_report_as_markdown(report_data)
                        console.print("\n[bold cyan]Session Report:[/bold cyan]")
                        from rich.markdown import Markdown

                        console.print(Markdown(report_md))
                except ImportError:
                    pass  # rich.prompt not available
        except Exception as e:
            logger.debug(f"Session reporting failed: {e}")
