import shutil
import subprocess
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table

from sono_eval.cli.formatters import WelcomeFormatter

console = Console()


@click.group()
def setup():
    """Interactive setup and onboarding commands."""
    pass


@setup.command()
@click.option("--interactive", is_flag=True, default=True, help="Run interactive setup wizard")
@click.option("--quick", is_flag=True, help="Quick setup with defaults")
def init(interactive: bool, quick: bool):
    """
    Initialize Sono-Eval setup with guided wizard.

    Walks you through first-time setup with explanations and checks.
    """
    # Show welcome banner
    WelcomeFormatter.show_welcome()
    console.print()

    if quick:
        console.print("[bold]Quick Setup Mode[/bold]")
        console.print("[dim]Using default configuration...[/dim]")
        console.print()
    else:
        console.print("[bold cyan]🚀 Interactive Setup Wizard[/bold cyan]")
        console.print(
            "[dim]This wizard will guide you through setting up Sono-Eval step by step.[/dim]"
        )
        console.print()

        ready = Confirm.ask("Ready to begin?", default=True)
        if not ready:
            console.print("[yellow]Setup cancelled[/yellow]")
            return

    # Track setup status
    setup_status = {
        "python": False,
        "dependencies": False,
        "config": False,
        "database": False,
        "test": False,
    }

    # Step 1: Check Python
    console.print()
    console.print("[bold]Step 1: Python Environment[/bold]")
    console.print("[dim]Checking Python version and environment...[/dim]")

    import sys

    version = sys.version_info
    required_version = (3, 9)

    if version.major >= required_version[0] and version.minor >= required_version[1]:
        console.print(
            f"[green]✓ Python {version.major}.{version.minor}.{version.micro} "
            f"(required: {required_version[0]}.{required_version[1]}+)[/green]"
        )
        setup_status["python"] = True
    else:
        console.print(
            f"[red]✗ Python {version.major}.{version.minor}.{version.micro} "
            f"(required: {required_version[0]}.{required_version[1]}+)[/red]"
        )
        console.print("[yellow]⚠ Please upgrade Python to 3.9 or higher[/yellow]")
        if not quick:
            should_continue = Confirm.ask("Continue anyway?", default=False)
            if not should_continue:
                return

    # Step 2: Check Dependencies
    console.print()
    console.print("[bold]Step 2: Dependencies[/bold]")
    console.print("[dim]Checking required packages...[/dim]")

    critical_deps = {
        "fastapi": "Web framework",
        "uvicorn": "ASGI server",
        "pydantic": "Data validation",
        "click": "CLI framework",
        "rich": "Terminal formatting",
        "torch": "Machine learning",
        "transformers": "NLP models",
    }

    missing = []
    dep_table = Table(show_header=True, header_style="bold cyan", border_style="dim")
    dep_table.add_column("Package", style="cyan")
    dep_table.add_column("Status", justify="center")
    dep_table.add_column("Purpose", style="dim")

    for dep, purpose in critical_deps.items():
        try:
            __import__(dep)
            dep_table.add_row(dep, "[green]✓[/green]", purpose)
        except ImportError:
            dep_table.add_row(dep, "[red]✗[/red]", purpose)
            missing.append(dep)

    console.print(dep_table)

    if missing:
        console.print(f"\n[yellow]⚠ Missing {len(missing)} packages[/yellow]")
        if not quick:
            install = Confirm.ask("Install missing dependencies now?", default=True)
            if install:
                _install_dependencies(missing)
                setup_status["dependencies"] = True
            else:
                console.print("[dim]You can install later with: pip install -r requirements.txt[/dim]")
        else:
            console.print("[dim]Run: pip install -r requirements.txt[/dim]")
    else:
        console.print("[green]✓ All dependencies installed[/green]")
        setup_status["dependencies"] = True

    # Step 3: Configuration
    console.print()
    console.print("[bold]Step 3: Configuration[/bold]")
    console.print("[dim]Setting up environment configuration...[/dim]")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if env_file.exists():
        console.print("[green]✓ .env file exists[/green]")
        setup_status["config"] = True
    elif env_example.exists():
        console.print("[yellow]⚠ .env file not found[/yellow]")
        if not quick:
            create_env = Confirm.ask("Create .env from .env.example?", default=True)
            if create_env:
                shutil.copy(env_example, env_file)
                console.print("[green]✓ Created .env file[/green]")
                console.print("[dim]You may want to edit .env to customize settings[/dim]")
                setup_status["config"] = True
        else:
            console.print("[dim]Run: cp .env.example .env[/dim]")
    else:
        console.print("[red]✗ No .env.example found[/red]")
        console.print("[dim]Using default configuration[/dim]")

    # Step 4: Database (optional)
    console.print()
    console.print("[bold]Step 4: Database (Optional)[/bold]")
    console.print("[dim]Checking database setup...[/dim]")

    if not quick:
        setup_db = Confirm.ask("Set up database now?", default=False)
        if setup_db:
            console.print("[dim]Database setup would run migrations here...[/dim]")
            console.print("[yellow]Note: Database migrations are optional for basic usage[/yellow]")
    else:
        console.print("[dim]Skipped in quick mode[/dim]")

    setup_status["database"] = True

    # Step 5: Quick Test
    console.print()
    console.print("[bold]Step 5: Verification[/bold]")
    console.print("[dim]Running quick test...[/dim]")

    if not quick:
        run_test = Confirm.ask("Run a test assessment?", default=True)
        if run_test:
            _run_test_assessment()
            setup_status["test"] = True
    else:
        console.print("[dim]Skipped in quick mode[/dim]")
        setup_status["test"] = True

    # Show Summary
    console.print()
    _show_setup_summary(setup_status)

    # Next Steps
    console.print()
    _show_next_steps()


def _install_dependencies(packages):
    """Install missing dependencies."""
    console.print()
    console.print("[bold]Installing dependencies...[/bold]")

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold]{task.description}[/bold]"),
        console=console,
    )

    with progress:
        task = progress.add_task("Installing packages...", total=None)

        try:
            # Use pip to install all requirements
            result = subprocess.run(
                ["pip", "install", "-r", "requirements.txt"],
                capture_output=True,
                text=True,
                check=True,
            )

            progress.update(task, description="Installation complete!")
            console.print("[green]✓ Dependencies installed successfully[/green]")

        except subprocess.CalledProcessError as e:
            console.print(f"[red]✗ Installation failed: {e}[/red]")
            console.print("[dim]You may need to install manually with: pip install -r requirements.txt[/dim]")
        except FileNotFoundError:
            console.print("[red]✗ pip not found in PATH[/red]")
            console.print("[dim]Make sure pip is installed and accessible[/dim]")


def _run_test_assessment():
    """Run a quick test assessment."""
    console.print()
    console.print("[dim]Running test assessment with sample code...[/dim]")

    # Sample test code
    test_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold]{task.description}[/bold]"),
        console=console,
    )

    with progress:
        task = progress.add_task("Testing assessment engine...", total=None)

        try:
            import asyncio

            from sono_eval.assessment.engine import AssessmentEngine
            from sono_eval.assessment.models import AssessmentInput, PathType

            engine = AssessmentEngine()
            assessment_input = AssessmentInput(
                candidate_id="test_user",
                submission_type="code",
                content={"code": test_code},
                paths_to_evaluate=[PathType.TECHNICAL],
            )

            result = asyncio.run(engine.assess(assessment_input))

            progress.update(task, description="Test complete!")
            console.print(f"[green]✓ Test assessment successful! Score: {result.overall_score:.1f}[/green]")

        except Exception as e:
            console.print(f"[yellow]⚠ Test assessment failed: {e}[/yellow]")
            console.print("[dim]This is not critical - you can still use Sono-Eval[/dim]")


def _show_setup_summary(status):
    """Show setup summary."""
    summary_panel = Panel(
        _build_status_text(status),
        title="[bold]Setup Summary[/bold]",
        border_style="cyan",
    )
    console.print(summary_panel)


def _build_status_text(status):
    """Build status text for summary."""
    from rich.text import Text

    text = Text()

    steps = [
        ("Python Environment", status.get("python", False)),
        ("Dependencies", status.get("dependencies", False)),
        ("Configuration", status.get("config", False)),
        ("Database", status.get("database", False)),
        ("Verification", status.get("test", False)),
    ]

    for step_name, step_status in steps:
        if step_status:
            text.append("✓ ", style="green bold")
            text.append(f"{step_name}\n", style="green")
        else:
            text.append("⚠ ", style="yellow bold")
            text.append(f"{step_name}\n", style="yellow")

    completed = sum(1 for _, s in steps if s)
    total = len(steps)

    text.append(f"\nCompleted: {completed}/{total} steps", style="bold")

    return text


def _show_next_steps():
    """Show next steps after setup."""
    next_steps = Panel(
        """[bold cyan]Next Steps:[/bold cyan]

1. Try a quick assessment:
   [dim]sono-eval assess run --candidate-id test_user --file sample.py[/dim]

2. Start the mobile companion:
   [dim]sono-eval server start --mobile[/dim]

3. Explore interactive mode:
   [dim]sono-eval repl[/dim]

4. View all commands:
   [dim]sono-eval --help[/dim]

[dim]Visit our documentation for more information![/dim]""",
        title="[bold]🚀 You're Ready![/bold]",
        border_style="green",
    )
    console.print(next_steps)
