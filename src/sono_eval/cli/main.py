"""
Command-line interface for Sono-Eval.

Provides commands for assessments, candidate management, and configuration.
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from tabulate import tabulate

from sono_eval.assessment.engine import AssessmentEngine
from sono_eval.assessment.models import AssessmentInput, PathType
from sono_eval.memory.memu import MemUStorage
from sono_eval.tagging.generator import TagGenerator
from sono_eval.utils.config import get_config

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """Sono-Eval: Explainable Multi-Path Developer Assessment System"""
    pass


# Assessment Commands
@cli.group()
def assess():
    """Assessment commands"""
    pass


@assess.command()
@click.option("--candidate-id", required=True, help="Candidate identifier")
@click.option("--file", type=click.Path(exists=True), help="Code file to assess")
@click.option("--content", help="Content to assess")
@click.option("--type", default="code", help="Submission type")
@click.option("--paths", multiple=True, help="Paths to evaluate")
@click.option("--output", type=click.Path(), help="Output file for results")
def run(candidate_id: str, file: Optional[str], content: Optional[str], 
        type: str, paths: tuple, output: Optional[str]):
    """Run an assessment"""
    console.print(f"[bold blue]Running assessment for candidate: {candidate_id}[/bold blue]")
    
    # Get content
    if file:
        with open(file, "r") as f:
            content = f.read()
    elif not content:
        console.print("[red]Error: Must provide either --file or --content[/red]")
        return
    
    # Parse paths
    path_list = [PathType[p.upper()] for p in paths] if paths else list(PathType)
    
    # Create assessment input
    assessment_input = AssessmentInput(
        candidate_id=candidate_id,
        submission_type=type,
        content={"code": content},
        paths_to_evaluate=path_list,
    )
    
    # Run assessment
    engine = AssessmentEngine()
    result = asyncio.run(engine.assess(assessment_input))
    
    # Display results
    console.print(f"\n[bold green]Assessment Complete![/bold green]")
    console.print(f"Overall Score: [bold]{result.overall_score:.2f}/100[/bold]")
    console.print(f"Confidence: {result.confidence:.2%}")
    console.print(f"\nSummary: {result.summary}")
    
    # Path scores table
    if result.path_scores:
        console.print("\n[bold]Path Scores:[/bold]")
        table = Table(show_header=True)
        table.add_column("Path")
        table.add_column("Score")
        table.add_column("Metrics")
        
        for ps in result.path_scores:
            table.add_row(
                ps.path.value,
                f"{ps.overall_score:.2f}",
                str(len(ps.metrics))
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
            console.print(f"  • {rec}")
    
    # Save to file if requested
    if output:
        with open(output, "w") as f:
            json.dump(result.model_dump(mode="json"), f, indent=2, default=str)
        console.print(f"\n[green]Results saved to {output}[/green]")


# Candidate Management Commands
@cli.group()
def candidate():
    """Candidate management commands"""
    pass


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
@click.option("--data", help="Initial data (JSON string)")
def create(candidate_id: str, data: Optional[str]):
    """Create a new candidate"""
    storage = MemUStorage()
    
    initial_data = None
    if data:
        initial_data = json.loads(data)
    
    memory = storage.create_candidate_memory(candidate_id, initial_data)
    console.print(f"[green]Created candidate: {memory.candidate_id}[/green]")


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
def show(candidate_id: str):
    """Show candidate information"""
    storage = MemUStorage()
    memory = storage.get_candidate_memory(candidate_id)
    
    if not memory:
        console.print(f"[red]Candidate not found: {candidate_id}[/red]")
        return
    
    console.print(f"\n[bold]Candidate: {memory.candidate_id}[/bold]")
    console.print(f"Last Updated: {memory.last_updated}")
    console.print(f"Nodes: {len(memory.nodes)}")
    console.print(f"Version: {memory.version}")
    
    # Show root data
    if memory.root_node.data:
        console.print("\n[bold]Root Data:[/bold]")
        console.print(json.dumps(memory.root_node.data, indent=2))


@candidate.command()
def list():
    """List all candidates"""
    storage = MemUStorage()
    candidates = storage.list_candidates()
    
    if not candidates:
        console.print("[yellow]No candidates found[/yellow]")
        return
    
    console.print(f"\n[bold]Candidates ({len(candidates)}):[/bold]")
    for candidate_id in candidates:
        console.print(f"  • {candidate_id}")


@candidate.command()
@click.option("--id", "candidate_id", required=True, help="Candidate ID")
@click.confirmation_option(prompt="Are you sure you want to delete this candidate?")
def delete(candidate_id: str):
    """Delete a candidate"""
    storage = MemUStorage()
    success = storage.delete_candidate_memory(candidate_id)
    
    if success:
        console.print(f"[green]Deleted candidate: {candidate_id}[/green]")
    else:
        console.print(f"[red]Candidate not found: {candidate_id}[/red]")


# Tagging Commands
@cli.group()
def tag():
    """Tagging commands"""
    pass


@tag.command()
@click.option("--file", type=click.Path(exists=True), help="File to tag")
@click.option("--text", help="Text to tag")
@click.option("--max-tags", default=5, help="Maximum tags to generate")
def generate(file: Optional[str], text: Optional[str], max_tags: int):
    """Generate tags for code or text"""
    if file:
        with open(file, "r") as f:
            text = f.read()
    elif not text:
        console.print("[red]Error: Must provide either --file or --text[/red]")
        return
    
    generator = TagGenerator()
    tags = generator.generate_tags(text, max_tags=max_tags)
    
    console.print(f"\n[bold]Generated Tags:[/bold]")
    for tag in tags:
        console.print(
            f"  • [cyan]{tag.tag}[/cyan] "
            f"[dim]({tag.category}, confidence: {tag.confidence:.2f})[/dim]"
        )


# Server Commands
@cli.group()
def server():
    """Server management commands"""
    pass


@server.command()
@click.option("--host", default=None, help="Host to bind to")
@click.option("--port", default=None, type=int, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
def start(host: Optional[str], port: Optional[int], reload: bool):
    """Start the API server"""
    import uvicorn
    from sono_eval.utils.config import get_config
    
    config = get_config()
    
    host = host or config.api_host
    port = port or config.api_port
    
    console.print(f"[bold green]Starting Sono-Eval API server...[/bold green]")
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
def config():
    """Configuration commands"""
    pass


@config.command()
def show():
    """Show current configuration"""
    cfg = get_config()
    
    console.print("\n[bold]Sono-Eval Configuration[/bold]\n")
    
    config_data = {
        "Application": {
            "Name": cfg.app_name,
            "Environment": cfg.app_env,
            "Debug": cfg.debug,
        },
        "API": {
            "Host": cfg.api_host,
            "Port": cfg.api_port,
            "Workers": cfg.api_workers,
        },
        "Assessment": {
            "Version": cfg.assessment_engine_version,
            "Multi-Path": cfg.assessment_multi_path_tracking,
            "Explanations": cfg.assessment_enable_explanations,
            "Dark Horse": cfg.dark_horse_mode,
        },
        "Storage": {
            "Memory Path": cfg.memu_storage_path,
            "Cache Size": cfg.memu_cache_size,
        },
    }
    
    for section, values in config_data.items():
        console.print(f"[bold cyan]{section}:[/bold cyan]")
        for key, value in values.items():
            console.print(f"  {key}: {value}")
        console.print()


if __name__ == "__main__":
    cli()
