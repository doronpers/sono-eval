"""
Command-line interface for Sono-Eval.

Provides commands for assessments, candidate management, and configuration.
"""

import click
from rich.console import Console

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
