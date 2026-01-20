"""
Interactive CLI onboarding for Sono-Eval.

Provides guided first-run experience with step-by-step setup.
"""

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from sono_eval.utils.config import get_config
from sono_eval.utils.logger import get_logger

console = Console()
logger = get_logger(__name__)


def print_welcome():
    """Print welcome message for first-time setup."""
    welcome_text = """
    Sono-Eval Setup
    ---------------
    This process will configure your local environment for assessment.
    """
    console.print(Panel(welcome_text, border_style="dim"))


def check_python_version() -> bool:
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        console.print(f"Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        console.print(
            f"[red]✗[/red] Python {version.major}.{version.minor}.{version.micro} detected. "
            "Python 3.8+ is required."
        )
        return False


def check_dependencies() -> bool:
    """Check if required dependencies are installed."""
    console.print("\n[bold]Checking dependencies...[/bold]")

    required_packages = [
        ("fastapi", "FastAPI"),
        ("pydantic", "Pydantic"),
        ("click", "Click"),
    ]

    all_ok = True
    for package, name in required_packages:
        try:
            __import__(package)
            console.print(f"✓ {name} installed")
        except ImportError:
            console.print(f"✗ {name} not found")
            all_ok = False

    if not all_ok:
        console.print(
            "\n[yellow]Tip:[/yellow] Install missing dependencies with: "
            "[cyan]pip install -r requirements.txt[/cyan]"
        )

    return all_ok


def setup_configuration() -> dict:
    """Interactive configuration setup."""
    console.print("\n[bold]Configuration Setup[/bold]")
    console.print("We'll configure your Sono-Eval environment.\n")

    config = {}

    # API Configuration
    console.print("[cyan]API Configuration[/cyan]")
    config["api_host"] = Prompt.ask(
        "API Host",
        default="0.0.0.0",  # nosec B104
        show_default=True,
    )
    config["api_port"] = int(
        Prompt.ask(
            "API Port",
            default="8000",
            show_default=True,
        )
    )

    # Storage Configuration
    console.print("\n[cyan]Storage Configuration[/cyan]")
    default_storage = str(Path.home() / ".sono-eval" / "storage")
    storage_path = Prompt.ask(
        "Storage Path",
        default=default_storage,
        show_default=True,
    )
    config["memu_storage_path"] = storage_path

    # Create storage directory if it doesn't exist
    storage_dir = Path(storage_path)
    if not storage_dir.exists():
        if Confirm.ask(f"\nCreate storage directory at {storage_path}?"):
            storage_dir.mkdir(parents=True, exist_ok=True)
            console.print("[green]✓[/green] Created storage directory")
        else:
            console.print(
                "[yellow]⚠[/yellow] Storage directory not created. "
                "You may need to create it manually."
            )

    return config


def explain_next_steps():
    """Explain what happens next."""
    console.print("\n[bold cyan]What's Next?[/bold cyan]\n")

    steps = [
        (
            "1",
            "Run your first assessment",
            "sono-eval assess run --candidate-id your_id --file solution.py",
        ),
        ("2", "View assessment results", "sono-eval assess get --assessment-id <id>"),
        (
            "3",
            "Explore the mobile interface",
            "Start the API: sono-eval api serve, then visit http://localhost:8000/mobile",
        ),
        ("4", "Get help anytime", "sono-eval --help or sono-eval <command> --help"),
    ]

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Step", style="cyan", width=4)
    table.add_column("Action", style="bold")
    table.add_column("Command", style="dim")

    for step, action, command in steps:
        table.add_row(step, action, command)

    console.print(table)

    console.print(
        "\n[yellow]💡 Tip:[/yellow] Use [cyan]sono-eval --help[/cyan] to see all available commands."
    )


def run_interactive_setup():
    """Run the complete interactive setup process."""
    print_welcome()

    # Step 1: Check Python version
    console.print("\n[bold]Step 1: Checking Python Version[/bold]")
    if not check_python_version():
        console.print("\n[red]Setup cannot continue. Please install Python 3.8 or higher.[/red]")
        sys.exit(1)

    # Step 2: Check dependencies
    console.print("\n[bold]Step 2: Checking Dependencies[/bold]")
    deps_ok = check_dependencies()
    if not deps_ok:
        if not Confirm.ask("\nContinue setup anyway? (You can install dependencies later)"):
            console.print("[yellow]Setup cancelled.[/yellow]")
            sys.exit(0)

    # Step 3: Configuration
    console.print("\n[bold]Step 3: Configuration[/bold]")
    if Confirm.ask("\nWould you like to configure Sono-Eval now?", default=True):
        setup_configuration()
        console.print("\n[green]✓[/green] Configuration complete")
        console.print(
            "\n[yellow]Note:[/yellow] Configuration values are stored in environment variables. "
            "You can modify them later or use configuration files."
        )
    else:
        console.print("\n[yellow]Skipping configuration. Using defaults.[/yellow]")

    # Step 4: Validation
    console.print("\n[bold]Step 4: Validating Setup[/bold]")
    try:
        cfg = get_config()
        console.print("[green]✓[/green] Configuration loaded successfully")
        console.print(f"[green]✓[/green] Storage path: {cfg.memu_storage_path}")
    except Exception as e:
        console.print(f"[yellow]⚠[/yellow] Configuration validation warning: {e}")
        console.print("[dim]You can continue, but some features may not work correctly.[/dim]")

    # Final step: Next steps
    explain_next_steps()

    console.print("\nSetup Complete.")
    console.print("You are ready to use Sono-Eval.\n")


@click.command()
@click.option(
    "--skip-checks",
    is_flag=True,
    help="Skip dependency and version checks",
)
def setup(skip_checks: bool):
    """
    Interactive setup wizard for Sono-Eval.

    Guides you through first-time configuration and validates your environment.

    Examples:

        # Run full interactive setup
        sono-eval setup

        # Skip dependency checks
        sono-eval setup --skip-checks
    """
    try:
        if skip_checks:
            console.print("[yellow]Skipping checks...[/yellow]\n")
            setup_configuration()
            explain_next_steps()
        else:
            run_interactive_setup()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Setup cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Setup error: {e}", exc_info=True)
        console.print(f"\n[red]Error during setup: {e}[/red]")
        console.print("[yellow]You can try running setup again or configure manually.[/yellow]")
        sys.exit(1)
