from typing import Optional

import click
from rich.console import Console
from rich.table import Table

from sono_eval.tagging.generator import TagGenerator

console = Console()


@click.group()
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
                content_text = f.read()
            if not content_text.strip():
                console.print("[red]Error: File is empty[/red]")
                raise click.Abort()
        elif not text:
            console.print("[red]Error: Must provide either --file or --text[/red]")
            console.print(
                "[yellow]Hint: Use --file path/to/file.py or --text 'your code here'[/yellow]"
            )
            raise click.Abort()
        else:
            content_text = text
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
        tags = generator.generate_tags(content_text, max_tags=max_tags)

        if quiet:
            # Just print tags, one per line
            for tag_item in tags:
                console.print(tag_item.tag)
        else:
            console.print(f"\n[bold green]Generated Tags ({len(tags)}):[/bold green]")
            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Tag", style="cyan")
            table.add_column("Category", style="yellow")
            table.add_column("Confidence", justify="right", style="green")

            if verbose:
                table.add_column("Context", style="dim", max_width=40)

            for tag_item in tags:
                row = [
                    tag_item.tag,
                    tag_item.category,
                    f"{tag_item.confidence:.2%}",
                ]
                if verbose:
                    context = (
                        tag_item.context[:40] + "..."
                        if tag_item.context and len(tag_item.context) > 40
                        else (tag_item.context or "")
                    )
                    row.append(context)
                table.add_row(*row)
            console.print(table)
    except Exception as e:
        console.print(f"[red]Error generating tags: {e}[/red]")
        raise click.Abort()
