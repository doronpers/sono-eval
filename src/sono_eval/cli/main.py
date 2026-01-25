"""
Command-line interface for Sono-Eval.

Provides commands for assessments, candidate management, and configuration.
"""

import click
from rich.console import Console
import sys
import io

# Handle internal encoding for Windows consoles
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, io.UnsupportedOperation):
        pass

# Import command groups
from sono_eval.cli.commands.assess import assess
from sono_eval.cli.commands.candidate import candidate
from sono_eval.cli.commands.server import server
from sono_eval.cli.commands.session import session
from sono_eval.cli.commands.setup import setup
from sono_eval.cli.commands.tag import tag

console = Console()


@click.group()
@click.version_option(version="0.1.1")
def cli():
    """Sono-Eval: Explainable Multi-Path Developer Assessment System."""
    pass


# Register command groups
cli.add_command(assess)
cli.add_command(candidate)
cli.add_command(server)
cli.add_command(tag)
cli.add_command(setup)
cli.add_command(session)

# Add interactive setup command to the existing setup group
try:
    from sono_eval.cli.onboarding import setup as interactive_setup_command

<<<<<<< Updated upstream
=======
    # Add to the existing setup group
>>>>>>> Stashed changes
    setup.add_command(interactive_setup_command, name="interactive")
except ImportError:
    pass


<<<<<<< Updated upstream
=======
# Assessment Commands
@cli.group()
def assess():
    """Assessment commands."""
    pass


@assess.command()
@click.option("--candidate-id", required=True, help="Candidate identifier")
@click.option("--file", type=click.Path(exists=True), help="Code file to assess")
@click.option("--content", help="Content to assess")
@click.option(
    "--type", default="code", help="Submission type (code, project, interview, portfolio, test)"
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
    paths: tuple,
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
                content = f.read()
            if not content.strip():
                console.print("[red]Error: File is empty[/red]")
                raise click.Abort()
        elif not content:
            console.print("[red]Error: Must provide either --file or --content[/red]")
            console.print(
                "[yellow]Hint: Use --file path/to/file.py or --content 'your code here'[/yellow]"
            )
            raise click.Abort()
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
            content={"code": content},
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
                    else "yellow" if ps.overall_score >= 60 else "red"
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


# Candidate Management Commands
@cli.group()
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
            console.print(f"[yellow]Warning: Candidate '{candidate_id}' already exists[/yellow]")
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
            console.print("[dim]Use 'sono-eval candidate create' to create a candidate[/dim]")
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
@click.option("--format", "output_format", type=click.Choice(["table", "json"]), default="table")
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
            console.print(f"\n[bold cyan]Assessment History for {candidate_id}[/bold cyan]")
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
                score_color = "green" if score >= 75 else "yellow" if score >= 60 else "red"

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
                    sum(scores[3:]) / max(1, len(scores) - 3) if len(scores) > 3 else recent_avg
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
            from rich.markdown import Markdown

            console.print(Markdown(report_content))

    except Exception as e:
        console.print(f"[red]Error generating report: {e}[/red]")
        raise click.Abort()


# Tagging Commands
@cli.group()
def tag():
    """Tagging commands."""
    pass


@tag.command()
@click.option("--file", type=click.Path(exists=True), help="File to tag")
@click.option("--text", help="Text to tag")
@click.option("--max-tags", default=5, help="Maximum tags to generate (1-20)")
@click.option("--quiet", is_flag=True, help="Quiet mode - just print tags")
@click.option("--verbose", is_flag=True, help="Verbose mode - show details")
def generate(file: Optional[str], text: Optional[str], max_tags: int, quiet: bool, verbose: bool):
    """
    Generate semantic tags for code or text.

    Examples:
        # Tag a file
        sono-eval tag generate --file solution.py

        # Tag inline text
        sono-eval tag generate --text "def hello(): return 'world'"

        # Generate more tags
        sono-eval tag generate --file solution.py --max-tags 10
    """
    if max_tags < 1 or max_tags > 20:
        console.print("[red]Error: --max-tags must be between 1 and 20[/red]")
        raise click.Abort()

    try:
        if file:
            if verbose:
                console.print(f"[dim]Reading file: {file}[/dim]")
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()
            if not text.strip():
                console.print("[red]Error: File is empty[/red]")
                raise click.Abort()
        elif not text:
            console.print("[red]Error: Must provide either --file or --text[/red]")
            console.print(
                "[yellow]Hint: Use --file path/to/file.py or --text 'your code here'[/yellow]"
            )
            raise click.Abort()
    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file}[/red]")
        raise click.Abort()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        raise click.Abort()

    try:
        if not quiet:
            console.print("[dim]Generating tags...[/dim]")
        generator = TagGenerator()
        tags = generator.generate_tags(text, max_tags=max_tags)

        if quiet:
            # Just print tags, one per line
            for tag in tags:
                console.print(tag.tag)
        else:
            console.print(f"\n[bold green]Generated Tags ({len(tags)}):[/bold green]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Tag", style="cyan")
            table.add_column("Category", style="yellow")
            table.add_column("Confidence", justify="right", style="green")

            if verbose:
                table.add_column("Context", style="dim", max_width=40)

            for tag in tags:
                row = [
                    tag.tag,
                    tag.category,
                    f"{tag.confidence:.2%}",
                ]
                if verbose:
                    context = (
                        tag.context[:40] + "..."
                        if tag.context and len(tag.context) > 40
                        else (tag.context or "")
                    )
                    row.append(context)
                table.add_row(*row)
            console.print(table)
    except Exception as e:
        console.print(f"[red]Error generating tags: {e}[/red]")
        raise click.Abort()


# Server Commands
@cli.group()
def server():
    """Server management commands."""
    pass


@server.command()
@click.option("--host", default=None, help="Host to bind to")
@click.option("--port", default=None, type=int, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def start(host: Optional[str], port: Optional[int], reload: bool):
    """Start the API server."""
    import uvicorn

    from sono_eval.utils.config import get_config

    config = get_config()

    host = host or config.api_host
    port = port or config.api_port

    console.print("[bold green]Starting Sono-Eval API server...[/bold green]")
    console.print(f"Host: {host}")
    console.print(f"Port: {port}")
    console.print(f"Reload: {reload}")

    uvicorn.run(
        "sono_eval.api.main:app",
        host=host,
        port=port,
        reload=reload,
    )


# Config Commands
@cli.group()
def setup():
    """Interactive setup and onboarding commands."""
    pass


@setup.command()
@click.option("--interactive", is_flag=True, help="Run interactive setup wizard")
def init(interactive: bool):
    """
    Initialize Sono-Eval setup (interactive mode).

    Guides you through first-time setup with explanations.
    """
    if interactive:
        console.print("\n[bold cyan]Sono-Eval Interactive Setup[/bold cyan]\n")
        console.print("This wizard will help you set up Sono-Eval step by step.\n")

        # Step 1: Check Python
        console.print("[bold]Step 1: Checking Python version...[/bold]")
        import sys

        version = sys.version_info
        if version.major == 3 and version.minor >= 9:
            console.print(
                f"[green]✓[/green] Python {version.major}.{version.minor}"
                f".{version.micro} (required: 3.9+)"
            )
        else:
            console.print(
                f"[red]✗[/red] Python {version.major}.{version.minor}"
                f".{version.micro} (required: 3.9+)"
            )
            console.print("[yellow]Please install Python 3.9 or higher[/yellow]")
            return

        # Step 2: Check dependencies
        console.print("\n[bold]Step 2: Checking dependencies...[/bold]")
        critical_deps = ["fastapi", "uvicorn", "pydantic", "click"]
        missing = []
        for dep in critical_deps:
            try:
                __import__(dep)
                console.print(f"[green]✓[/green] {dep}")
            except ImportError:
                console.print(f"[red]✗[/red] {dep} (missing)")
                missing.append(dep)

        if missing:
            console.print("\n[yellow]Installing missing dependencies...[/yellow]")
            console.print("[dim]Run: pip install -r requirements.txt[/dim]")
        else:
            console.print("[green]✓ All critical dependencies installed[/green]")

        # Step 3: Environment file
        console.print("\n[bold]Step 3: Checking configuration...[/bold]")

        env_file = Path(".env")
        env_example = Path(".env.example")
        if env_file.exists():
            console.print("[green]✓[/green] .env file exists")
        elif env_example.exists():
            console.print("[yellow]⚠[/yellow] .env file missing (but .env.example exists)")
            if click.confirm("Create .env from .env.example?"):
                import shutil

                shutil.copy(env_example, env_file)
                console.print("[green]✓[/green] .env file created")
        else:
            console.print("[yellow]⚠[/yellow] No .env file found (optional for development)")

        # Step 4: Data directories
        console.print("\n[bold]Step 4: Checking data directories...[/bold]")
        dirs = [Path("./data/memory"), Path("./data/tagstudio"), Path("./models/cache")]
        for dir_path in dirs:
            if dir_path.exists():
                console.print(f"[green]✓[/green] {dir_path} exists")
            else:
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    console.print(f"[green]✓[/green] {dir_path} created")
                except Exception as e:
                    console.print(f"[red]✗[/red] {dir_path} cannot be created: {e}")

        # Summary
        console.print("\n[bold green]✓ Setup Complete![/bold green]\n")
        console.print("Next steps:")
        console.print("  1. Start the server: [cyan]sono-eval server start[/cyan]")
        console.print("  2. Open in browser: [cyan]http://localhost:8000/mobile[/cyan]")
        console.print("  3. Complete your first assessment!")
        console.print(
            "\n[yellow]💡 Tip:[/yellow] Use [cyan]sono-eval --help[/cyan] "
            "to see all available commands\n"
        )
    else:
        console.print("[yellow]Run with --interactive flag for guided setup[/yellow]")
        console.print("[dim]Example: sono-eval setup init --interactive[/dim]")


@cli.group()
def config():
    """Manage configuration."""
    pass


@cli.group()
def insights():
    """Insights and analysis commands (hidden features)."""
    pass


@insights.command()
@click.option("--deep", is_flag=True, help="Deep analysis mode (easter egg)")
@click.option("--pattern-recognition", is_flag=True, help="Pattern recognition analysis")
def analyze(deep: bool, pattern_recognition: bool):
    """Unlock advanced analysis features (hidden command).

    Discovered by: sono-eval insights --deep.
    """
    if deep:
        console.print("[bold cyan]🔓 Expert Mode Unlocked![/bold cyan]")
        console.print("\n[bold]Deep Analysis Features:[/bold]")
        console.print("  • Raw metric data access")
        console.print("  • Cross-path comparison tools")
        console.print("  • Trend analysis over time")
        console.print("  • Pattern detection algorithms")
        console.print(
            "\n[yellow]Use these features to get deeper insights into assessments.[/yellow]"
        )
    elif pattern_recognition:
        console.print("[bold cyan]🔓 Pattern Recognition Unlocked![/bold cyan]")
        console.print("\n[bold]Pattern Analysis Features:[/bold]")
        console.print("  • Design pattern detection")
        console.print("  • Anti-pattern identification")
        console.print("  • Code smell analysis")
        console.print("  • Best practice recommendations")
    else:
        console.print("[yellow]Hint: Try --deep or --pattern-recognition flags[/yellow]")
        console.print("[dim]This is a hidden feature. Explore to discover more![/dim]")


>>>>>>> Stashed changes
@cli.command()
def repl():
    """Start interactive REPL mode for guided assessments."""
    from sono_eval.cli.repl import start_repl

    start_repl()


# Add interactive setup command if available (legacy compatibility)
try:
    from sono_eval.cli.onboarding import setup as interactive_setup_command

    # Add to the existing setup group if not already present
    # Note: Our new setup module handles the group, but we might want to keep
    # the onboarding module's specific command if it's different.
    # For now, we'll assume the new setup.py covers the basics and we can
    # alias 'interactive' if needed.
    setup.add_command(interactive_setup_command, name="interactive_legacy")
except ImportError:
    pass

if __name__ == "__main__":
    cli()
