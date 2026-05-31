"""
CLI entry point for Natural Language File Renamer.
"""

import click
from typing import List
from nl_renamer.transformer import rename_files


@click.command()
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--pattern", "-p", required=True, help="Natural language pattern (e.g., 'today's date + original name')")
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without actually renaming")
@click.version_option()

def cli(files: List[str], pattern: str, dry_run: bool):
    """Rename files using natural language patterns."""
    results = rename_files(files, pattern, dry_run)
    for result in results:
        click.echo(result)


if __name__ == "__main__":
    cli()