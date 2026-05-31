#!/usr/bin/env python3
"""
CLI interface for Natural Language File Renamer.
"""

import click
from .renamer import rename_files


@click.command()
@click.argument("command", type=str)
@click.option("--directory", "-d", default=".", help="Directory containing files to rename.")
@click.option("--dry-run", is_flag=True, help="Show changes without applying them.")
@click.option("--verbose", is_flag=True, help="Show detailed output.")
def cli(command: str, directory: str, dry_run: bool, verbose: bool):
    """Rename files using natural language."""
    if verbose:
        click.echo(f"Directory: {directory}")
        click.echo(f"Command: {command}")
    
    changes = rename_files(directory, command, dry_run)
    
    if not changes:
        click.echo("No changes to apply.")
        return
    
    for change in changes:
        click.echo(change)
    
    if dry_run:
        click.echo(f"\nDry run: {len(changes)} changes would be applied.")
    else:
        click.echo(f"\nApplied {len(changes)} changes.")


if __name__ == "__main__":
    cli()