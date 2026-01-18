from pathlib import Path

import click
from rich.console import Console

console = Console()


@click.group()
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
