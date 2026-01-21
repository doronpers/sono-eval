"""Interactive REPL mode for Sono-Eval.

Provides a guided, conversational interface for running assessments
and exploring results.
"""

import asyncio
import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.cli.formatters import (
    AssessmentFormatter,
    ErrorFormatter,
    InteractiveFormatter,
    ProgressFormatter,
    WelcomeFormatter,
)

console = Console()


class ReplSession:
    """Interactive REPL session for Sono-Eval."""

    def __init__(self):
        self.engine = AssessmentEngine()
        self.current_candidate = None
        self.last_result = None
        self.history = []

    def start(self):
        """Start the interactive REPL session."""
        WelcomeFormatter.show_welcome()
        console.print()
        console.print("[bold]Interactive Assessment Mode[/bold]")
        console.print("[dim]Type 'help' for available commands, 'exit' to quit[/dim]")
        console.print()

        while True:
            try:
                # Get command from user
                command = Prompt.ask("\n[bold cyan]sono-eval[/bold cyan]")

                # Handle empty input
                if not command.strip():
                    continue

                # Parse and execute command
                self.handle_command(command.strip())

            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Type 'exit' to quit.[/yellow]")
                continue
            except EOFError:
                console.print("\n[dim]Goodbye![/dim]")
                break

    def handle_command(self, command: str):
        """Handle a REPL command."""
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        # Command dispatch
        commands = {
            "help": self.cmd_help,
            "?": self.cmd_help,
            "assess": self.cmd_assess,
            "candidate": self.cmd_candidate,
            "paths": self.cmd_paths,
            "result": self.cmd_result,
            "history": self.cmd_history,
            "clear": self.cmd_clear,
            "exit": self.cmd_exit,
            "quit": self.cmd_exit,
        }

        handler = commands.get(cmd)
        if handler:
            handler(args)
        else:
            console.print(f"[red]Unknown command: {cmd}[/red]")
            console.print("[dim]Type 'help' for available commands[/dim]")

    def cmd_help(self, args: str):
        """Show help information."""
        help_table = Table(
            title="[bold]Available Commands[/bold]",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
        )

        help_table.add_column("Command", style="cyan", no_wrap=True)
        help_table.add_column("Description", style="dim")

        commands = [
            ("assess", "Start a new assessment (guided)"),
            ("assess <file>", "Assess a specific file"),
            ("candidate <id>", "Set current candidate ID"),
            ("paths", "Show available assessment paths"),
            ("result", "Show last assessment result"),
            ("history", "Show assessment history"),
            ("clear", "Clear the screen"),
            ("help, ?", "Show this help message"),
            ("exit, quit", "Exit the REPL"),
        ]

        for cmd, desc in commands:
            help_table.add_row(cmd, desc)

        console.print(help_table)

    def cmd_assess(self, args: str):
        """Run an assessment."""
        # Set candidate ID if not set
        if not self.current_candidate:
            candidate_id = Prompt.ask(
                "[bold]Enter candidate ID[/bold]",
                default="guest",
            )
            self.current_candidate = candidate_id
        else:
            console.print(f"[dim]Assessing candidate: {self.current_candidate}[/dim]")

        # Get file or content
        if args:
            file_path = Path(args)
            if not file_path.exists():
                ErrorFormatter.format_file_error(args, "not_found")
                return

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                ErrorFormatter.format_error(
                    error_type="File Error",
                    message=f"Error reading file: {e}",
                )
                return
        else:
            # Ask for file path
            use_file = Confirm.ask("Do you want to assess a file?", default=True)

            if use_file:
                file_path_str = Prompt.ask("[bold]Enter file path[/bold]")
                file_path = Path(file_path_str)

                if not file_path.exists():
                    ErrorFormatter.format_file_error(file_path_str, "not_found")
                    return

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                except Exception as e:
                    ErrorFormatter.format_error(
                        error_type="File Error",
                        message=f"Error reading file: {e}",
                    )
                    return
            else:
                console.print("[bold]Enter content (Ctrl+D when done):[/bold]")
                lines = []
                try:
                    while True:
                        line = input()
                        lines.append(line)
                except EOFError:
                    pass
                content = "\n".join(lines)

        if not content.strip():
            console.print("[red]No content provided[/red]")
            return

        # Select paths
        console.print()
        InteractiveFormatter.show_path_selection_menu()

        use_all_paths = Confirm.ask(
            "Assess all paths?",
            default=True,
        )

        if use_all_paths:
            path_list = list(PathType)
        else:
            console.print(
                "[dim]Enter path numbers (comma-separated): "
                "1=technical, 2=design, 3=collaboration, 4=problem_solving, 5=communication[/dim]"
            )
            path_input = Prompt.ask("Paths", default="1,2,3,4,5")
            path_map = {
                "1": PathType.TECHNICAL,
                "2": PathType.DESIGN,
                "3": PathType.COLLABORATION,
                "4": PathType.PROBLEM_SOLVING,
                "5": PathType.COMMUNICATION,
            }
            path_list = [
                path_map[p.strip()] for p in path_input.split(",") if p.strip() in path_map
            ]

        # Create assessment input
        assessment_input = AssessmentInput(
            candidate_id=self.current_candidate,
            submission_type="code",
            content={"code": content},
            paths_to_evaluate=path_list,
        )

        # Run assessment with progress
        console.print()
        progress = ProgressFormatter.create_assessment_progress()
        with progress:
            task = progress.add_task("Running assessment...", total=len(path_list) + 1)

            try:
                result = asyncio.run(self.engine.assess(assessment_input))
                progress.update(
                    task, advance=len(path_list) + 1, description="Assessment complete!"
                )
            except Exception as e:
                ErrorFormatter.format_error(
                    error_type="Assessment Error",
                    message=f"Error running assessment: {e}",
                )
                return

        # Store result
        self.last_result = result
        self.history.append(
            {
                "candidate_id": self.current_candidate,
                "score": result.overall_score,
                "timestamp": result.timestamp,
            }
        )

        # Display result
        AssessmentFormatter.format_complete_result(result, verbose=True)

    def cmd_candidate(self, args: str):
        """Set or show current candidate."""
        if args:
            self.current_candidate = args
            console.print(f"[green]✓ Current candidate set to: {args}[/green]")
        else:
            if self.current_candidate:
                console.print(f"Current candidate: [cyan]{self.current_candidate}[/cyan]")
            else:
                console.print("[yellow]No candidate set. Use: candidate <id>[/yellow]")

    def cmd_paths(self, args: str):
        """Show available assessment paths."""
        console.print()
        InteractiveFormatter.show_path_selection_menu()

    def cmd_result(self, args: str):
        """Show last assessment result."""
        if self.last_result:
            AssessmentFormatter.format_complete_result(self.last_result, verbose=True)
        else:
            console.print("[yellow]No assessment result available yet[/yellow]")
            console.print("[dim]Run an assessment with the 'assess' command[/dim]")

    def cmd_history(self, args: str):
        """Show assessment history."""
        if not self.history:
            console.print("[yellow]No assessment history yet[/yellow]")
            return

        table = Table(
            title="[bold]Assessment History[/bold]",
            show_header=True,
            header_style="bold cyan",
        )

        table.add_column("#", style="dim", width=4)
        table.add_column("Candidate", style="cyan")
        table.add_column("Score", justify="right")
        table.add_column("Time", style="dim")

        for i, entry in enumerate(self.history[-10:], 1):  # Last 10
            score = entry["score"]
            score_color = AssessmentFormatter._get_score_color(score)
            table.add_row(
                str(i),
                entry["candidate_id"],
                f"[{score_color}]{score:.1f}[/{score_color}]",
                entry["timestamp"].strftime("%H:%M:%S"),
            )

        console.print(table)

    def cmd_clear(self, args: str):
        """Clear the screen."""
        console.clear()

    def cmd_exit(self, args: str):
        """Exit the REPL."""
        console.print("[dim]Goodbye![/dim]")
        sys.exit(0)


def start_repl():
    """Start the interactive REPL."""
    session = ReplSession()
    session.start()


if __name__ == "__main__":
    start_repl()
