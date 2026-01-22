"""Rich formatters for beautiful CLI output.

This module provides enhanced formatting utilities using the Rich library
for a better developer experience in the CLI.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional

if TYPE_CHECKING:
    from sono_eval.cli.error_recovery import RecoverableError

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from sono_eval.assessment.models import AssessmentResult, PathScore, PathType

console = Console()


class AssessmentFormatter:
    """Format assessment results with rich visual elements."""

    # Color schemes for different score ranges
    SCORE_COLORS = {
        "excellent": "#22c55e",  # green
        "good": "#3b82f6",  # blue
        "average": "#f59e0b",  # amber
        "poor": "#ef4444",  # red
    }

    PATH_COLORS = {
        PathType.TECHNICAL: "#3b82f6",  # blue
        PathType.DESIGN: "#8b5cf6",  # purple
        PathType.COLLABORATION: "#22c55e",  # green
        PathType.PROBLEM_SOLVING: "#f59e0b",  # amber
        PathType.COMMUNICATION: "#06b6d4",  # cyan
    }

    PATH_ICONS = {
        PathType.TECHNICAL: "⚙️",
        PathType.DESIGN: "🎨",
        PathType.COLLABORATION: "🤝",
        PathType.PROBLEM_SOLVING: "🧩",
        PathType.COMMUNICATION: "💬",
    }

    @staticmethod
    def _get_score_color(score: float) -> str:
        """Get color for a score value."""
        if score >= 85:
            return AssessmentFormatter.SCORE_COLORS["excellent"]
        elif score >= 70:
            return AssessmentFormatter.SCORE_COLORS["good"]
        elif score >= 60:
            return AssessmentFormatter.SCORE_COLORS["average"]
        else:
            return AssessmentFormatter.SCORE_COLORS["poor"]

    @staticmethod
    def _get_score_emoji(score: float) -> str:
        """Get emoji for a score value."""
        if score >= 90:
            return "🌟"
        elif score >= 80:
            return "💪"
        elif score >= 70:
            return "✓"
        elif score >= 60:
            return "📈"
        else:
            return "🎯"

    @classmethod
    def format_overall_score(cls, result: AssessmentResult) -> Panel:
        """Format overall score in a beautiful panel."""
        score_color = cls._get_score_color(result.overall_score)
        score_emoji = cls._get_score_emoji(result.overall_score)

        # Create score display
        score_text = Text()
        score_text.append(f"{score_emoji} ", style="bold")
        score_text.append(f"{result.overall_score:.1f}", style=f"bold {score_color}")
        score_text.append("/100", style="dim")

        # Confidence indicator
        confidence_pct = result.confidence * 100
        confidence_color = (
            "green" if confidence_pct >= 80 else "yellow" if confidence_pct >= 60 else "red"
        )
        confidence_text = Text()
        confidence_text.append("Confidence: ", style="dim")
        confidence_text.append(f"{confidence_pct:.0f}%", style=confidence_color)

        # Build panel content
        content = Text()
        content.append(score_text)
        content.append("\n")
        content.append(confidence_text)

        return Panel(
            content,
            title="[bold]Overall Score[/bold]",
            border_style=score_color,
            padding=(1, 2),
        )

    @classmethod
    def format_path_scores(cls, path_scores: List[PathScore]) -> Table:
        """Format path scores in a detailed table."""
        table = Table(
            title="[bold]Assessment Breakdown[/bold]",
            show_header=True,
            header_style="bold cyan",
            border_style="cyan",
            padding=(0, 1),
        )

        table.add_column("Path", style="cyan", no_wrap=True, width=18)
        table.add_column("Score", justify="center", width=10)
        table.add_column("Grade", justify="center", width=8)
        table.add_column("Metrics", justify="center", width=10)
        table.add_column("Top Strength", style="dim", width=30)

        for ps in path_scores:
            # Path name with icon
            path_icon = cls.PATH_ICONS.get(ps.path, "📝")
            path_name = f"{path_icon} {ps.path.value.replace('_', ' ').title()}"

            # Score with color
            score_color = cls._get_score_color(ps.overall_score)
            score_display = f"[{score_color}]{ps.overall_score:.1f}[/{score_color}]"

            # Grade
            grade = cls._score_to_grade(ps.overall_score)
            grade_color = cls._get_score_color(ps.overall_score)
            grade_display = f"[{grade_color}]{grade}[/{grade_color}]"

            # Metrics count
            metrics_count = str(len(ps.metrics))

            # Top strength
            top_strength = ps.strengths[0] if ps.strengths else "-"
            if len(top_strength) > 28:
                top_strength = top_strength[:25] + "..."

            table.add_row(
                path_name,
                score_display,
                grade_display,
                metrics_count,
                top_strength,
            )

        return table

    @classmethod
    def format_findings(cls, result: AssessmentResult) -> Panel:
        """Format key findings in a panel."""
        tree = Tree("📋 [bold]Key Findings[/bold]")

        # Add strengths
        if result.key_findings:
            strengths_branch = tree.add("✅ [green]Highlights[/green]")
            for finding in result.key_findings[:5]:  # Limit to top 5
                strengths_branch.add(f"[dim]{finding}[/dim]")

        # Add recommendations
        if result.recommendations:
            recs_branch = tree.add("💡 [yellow]Recommendations[/yellow]")
            for rec in result.recommendations[:5]:  # Limit to top 5
                recs_branch.add(f"[dim]{rec}[/dim]")

        return Panel(tree, border_style="blue", padding=(1, 2))

    @classmethod
    def format_micro_motives(cls, result: AssessmentResult) -> Optional[Table]:
        """Format micro-motives in a table."""
        if not result.micro_motives:
            return None

        table = Table(
            title="[bold]🎯 Dark Horse Micro-Motives[/bold]",
            show_header=True,
            header_style="bold magenta",
            border_style="magenta",
        )

        table.add_column("Motive", style="magenta")
        table.add_column("Strength", justify="right", width=15)
        table.add_column("Signal", style="dim")

        for motive in result.micro_motives[:8]:  # Top 8
            # Strength bar
            strength_pct = int(motive.strength * 100)
            bar_length = int(strength_pct / 10)
            strength_bar = "█" * bar_length + "░" * (10 - bar_length)
            strength_display = f"{strength_bar} {strength_pct}%"

            # Motive name
            motive_name = motive.motive_type.value.replace("_", " ").title()

            # Signal description (if available)
            # Signal description (if available)
            evidence_text = (
                ", ".join(str(e) for e in motive.evidence)
                if isinstance(motive.evidence, list)
                else str(motive.evidence)
            )
            signal = evidence_text[:40] + "..." if len(evidence_text) > 40 else evidence_text

            table.add_row(motive_name, strength_display, signal)

        return table

    @classmethod
    def format_complete_result(cls, result: AssessmentResult, verbose: bool = False) -> None:
        """Format and display a complete assessment result."""
        console.print()
        console.print("[bold green]✓ Assessment Complete![/bold green]")
        console.print()

        # Overall score panel
        console.print(cls.format_overall_score(result))
        console.print()

        # Summary
        console.print(Panel(result.summary, title="[bold]Summary[/bold]", border_style="blue"))
        console.print()

        # Path scores table
        if result.path_scores:
            console.print(cls.format_path_scores(result.path_scores))
            console.print()

        # Findings panel
        console.print(cls.format_findings(result))
        console.print()

        # Micro-motives (if verbose)
        if verbose and result.micro_motives:
            motives_table = cls.format_micro_motives(result)
            if motives_table:
                console.print(motives_table)
                console.print()

        # Processing time
        if verbose and result.processing_time_ms:
            console.print(
                f"[dim]Processing time: {result.processing_time_ms:.2f}ms[/dim]",
                style="dim",
            )

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"


class ProgressFormatter:
    """Progress indicators for long-running operations."""

    @staticmethod
    def create_assessment_progress() -> Progress:
        """Create progress indicator for assessment."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}[/bold blue]"),
            BarColumn(),
            MofNCompleteColumn(),
            TextColumn("•"),
            TimeElapsedColumn(),
            console=console,
        )

    @staticmethod
    def create_simple_spinner(description: str) -> Progress:
        """Create simple spinner with description."""
        return Progress(
            SpinnerColumn(),
            TextColumn("[bold]{task.description}[/bold]"),
            console=console,
            transient=True,
        )


class ErrorFormatter:
    """Format errors with helpful context and suggestions."""

    @staticmethod
    def format_error(
        error_type: str,
        message: str,
        suggestions: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Format and display an error with suggestions."""
        # Error panel
        error_panel = Panel(
            f"[red]{message}[/red]",
            title=f"[bold red]❌ {error_type}[/bold red]",
            border_style="red",
        )
        console.print()
        console.print(error_panel)

        # Context information
        if context:
            console.print("\n[bold]Context:[/bold]")
            for key, value in context.items():
                console.print(f"  • {key}: [cyan]{value}[/cyan]")

        # Suggestions
        if suggestions:
            console.print("\n[bold yellow]💡 Suggestions:[/bold yellow]")
            for i, suggestion in enumerate(suggestions, 1):
                console.print(f"  {i}. {suggestion}")

        console.print()

    @staticmethod
    def format_validation_error(field: str, message: str, example: Optional[str] = None) -> None:
        """Format validation error with example."""
        suggestions = [
            f"Check the '{field}' parameter",
            "Run with --help for usage information",
        ]

        if example:
            suggestions.append(f"Example: {example}")

        ErrorFormatter.format_error(
            error_type="Validation Error",
            message=message,
            suggestions=suggestions,
            context={"field": field},
        )

    @staticmethod
    def format_file_error(file_path: str, error_type: str) -> None:
        """Format file-related error."""
        suggestions = []

        if error_type == "not_found":
            message = f"File not found: {file_path}"
            suggestions = [
                "Check that the file path is correct",
                "Use an absolute path or relative path from current directory",
                "Verify the file exists with: ls -la",
            ]
        elif error_type == "permission":
            message = f"Permission denied: {file_path}"
            suggestions = [
                "Check file permissions with: ls -l",
                "Ensure you have read access to the file",
                "Try running with appropriate permissions",
            ]
        elif error_type == "empty":
            message = f"File is empty: {file_path}"
            suggestions = [
                "Verify the file contains content",
                "Use --content flag to provide content directly",
            ]
        else:
            message = f"File error: {file_path}"
            suggestions = ["Check file accessibility and format"]

        ErrorFormatter.format_error(
            error_type="File Error",
            message=message,
            suggestions=suggestions,
            context={" file": file_path},
        )

    @staticmethod
    def format_recoverable_error(error: "RecoverableError") -> None:  # noqa: F821
        """
        Format and display a RecoverableError with recovery suggestions.

        Args:
            error: RecoverableError instance with recovery actions
        """
        from sono_eval.cli.error_recovery import ErrorSeverity

        # Choose colors based on severity
        severity_colors = {
            ErrorSeverity.INFO: "blue",
            ErrorSeverity.WARNING: "yellow",
            ErrorSeverity.ERROR: "red",
            ErrorSeverity.FATAL: "bold red",
        }
        severity_icons = {
            ErrorSeverity.INFO: "ℹ️",
            ErrorSeverity.WARNING: "⚠️",
            ErrorSeverity.ERROR: "❌",
            ErrorSeverity.FATAL: "🔥",
        }

        color = severity_colors.get(error.severity, "red")
        icon = severity_icons.get(error.severity, "❌")

        # Error panel
        error_panel = Panel(
            f"[{color}]{error.message}[/{color}]",
            title=(
                f"[bold {color}]{icon} "
                f"{error.error_type.replace('_', ' ').title()}[/bold {color}]"
            ),
            border_style=color,
        )
        console.print()
        console.print(error_panel)

        # Context information
        if error.context:
            console.print("\n[bold]Context:[/bold]")
            for key, value in error.context.items():
                if value is not None:  # Skip None values
                    console.print(f"  • {key}: [cyan]{value}[/cyan]")

        # Recovery actions
        if error.recovery_actions:
            console.print("\n[bold yellow]💡 Recovery Actions:[/bold yellow]")
            for i, action in enumerate(error.recovery_actions, 1):
                console.print(f"  {i}. {action}")

        # Retry command
        if error.retry_command:
            console.print("\n[bold green]🔄 Retry with:[/bold green]")
            console.print(f"  [cyan]{error.retry_command}[/cyan]")

        # Fatal error warning
        if error.is_fatal:
            console.print(
                "\n[bold red]⚠️  This is a fatal error that cannot be automatically recovered."
                "[/bold red]"
            )

        console.print()


class WelcomeFormatter:
    """Format welcome messages and help screens."""

    @staticmethod
    def show_welcome() -> None:
        """Display welcome message with quick start."""
        banner = (
            "\n"
            "[bold cyan]╔═══════════════════════════════════════════════════════╗[/bold cyan]\n"
            "[bold cyan]║[/bold cyan]  [bold white]Sono-Eval[/bold white] - "
            "Explainable Developer Assessment  [bold cyan]║[/bold cyan]\n"
            "[bold cyan]║[/bold cyan]  [dim]Multi-Path Evidence-Based Evaluation System[/dim]     "
            "[bold cyan]║[/bold cyan]\n"
            "[bold cyan]╚═══════════════════════════════════════════════════════╝[/bold cyan]\n"
        )
        console.print(banner)

    @staticmethod
    def show_quick_start() -> None:
        """Display quick start guide."""
        quick_start = Table(
            title="[bold]Quick Start Guide[/bold]",
            show_header=False,
            border_style="cyan",
            padding=(0, 2),
        )

        quick_start.add_column("Command", style="cyan", no_wrap=True)
        quick_start.add_column("Description", style="dim")

        commands = [
            ("sono-eval setup", "Interactive setup wizard"),
            ("sono-eval assess run", "Run an assessment"),
            ("sono-eval assess run --help", "See all assessment options"),
            ("sono-eval repl", "Enter interactive mode"),
            ("sono-eval --help", "View all commands"),
        ]

        for cmd, desc in commands:
            quick_start.add_row(f"[bold]{cmd}[/bold]", desc)

        console.print(quick_start)
        console.print()
        console.print(
            "[dim]Tip: Use --verbose for detailed output, --quiet for minimal output[/dim]"
        )
        console.print()


class InteractiveFormatter:
    """Format interactive prompts and menus."""

    @staticmethod
    def show_path_selection_menu() -> None:
        """Display path selection menu."""
        console.print("\n[bold]Select Assessment Paths:[/bold]\n")

        paths = [
            (
                "technical",
                "⚙️",
                "Technical Skills & Practices",
                "Code quality, patterns, testing",
            ),
            (
                "design",
                "🎨",
                "System Design & Architecture",
                "Design decisions, scalability",
            ),
            (
                "collaboration",
                "🤝",
                "Collaboration & Teamwork",
                "Communication, code review",
            ),
            (
                "problem_solving",
                "🧩",
                "Problem Solving",
                "Debugging, optimization, analysis",
            ),
            (
                "communication",
                "💬",
                "Communication",
                "Documentation, clarity, expression",
            ),
        ]

        for _, icon, title, desc in paths:
            console.print(f"{icon} [bold cyan]{title}[/bold cyan]")
            console.print(f"   [dim]{desc}[/dim]")
            console.print()
