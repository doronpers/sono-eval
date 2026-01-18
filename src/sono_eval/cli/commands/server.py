from typing import Optional

import click
from rich.console import Console

from sono_eval.utils.config import get_config

console = Console()


@click.group()
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
