"""Command-line interface for the platform."""

from __future__ import annotations

import logging

import typer

from handicraft_export_intelligence.logging_config import configure_logging
from handicraft_export_intelligence.settings import load_settings

app = typer.Typer(
    name="hei",
    help="Rajasthan Handicraft Export Intelligence Platform.",
    no_args_is_help=True,
)


@app.callback()
def main() -> None:
    """Initialize common CLI services."""

    configure_logging()


@app.command()
def info() -> None:
    """Show project configuration information."""

    settings = load_settings()
    logger = logging.getLogger(__name__)
    logger.info("Loaded settings for %s", settings.project.name)

    typer.echo(settings.project.name)
    typer.echo(f"Environment: {settings.project.environment}")
    typer.echo(f"Source data: {settings.paths.raw_workbook_dir}")


@app.command()
def validate() -> None:
    """Placeholder for validation workflows."""

    typer.echo("Validation command is wired. Business logic starts in a later sprint.")


@app.command("build-master")
def build_master() -> None:
    """Placeholder for master dataset workflows."""

    typer.echo("Master dataset command is wired. Business logic starts later.")


@app.command()
def analyze() -> None:
    """Placeholder for analytics workflows."""

    typer.echo("Analytics command is wired. Business logic starts later.")


@app.command()
def intelligence() -> None:
    """Placeholder for export intelligence workflows."""

    typer.echo("Intelligence command is wired. Business logic starts later.")


@app.command()
def report() -> None:
    """Placeholder for reporting workflows."""

    typer.echo("Reporting command is wired. Business logic starts later.")
