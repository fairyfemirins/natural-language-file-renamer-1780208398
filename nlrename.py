#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

A CLI tool to rename files using natural language expressions.
Example: `nlrename "today's date + original name" *.txt`
"""

import os
import re
import click
from datetime import datetime
from dateutil.parser import parse


@click.command()
@click.argument('pattern', type=str)
@click.argument('files', nargs=-1, type=click.Path(exists=True))
@click.option('--dry-run', is_flag=True, help="Preview changes without renaming.")
def cli(pattern: str, files: list, dry_run: bool):
    """Rename files using natural language patterns."""
    if not files:
        raise click.UsageError("No files provided.")

    for file_path in files:
        dir_name, old_name = os.path.split(file_path)
        new_name = apply_pattern(pattern, old_name)
        new_path = os.path.join(dir_name, new_name)

        if dry_run:
            click.echo(f"[DRY RUN] {old_name} -> {new_name}")
        else:
            os.rename(file_path, new_path)
            click.echo(f"Renamed: {old_name} -> {new_name}")


def apply_pattern(pattern: str, filename: str) -> str:
    """Apply natural language pattern to filename."""
    name, ext = os.path.splitext(filename)
    today = datetime.now().strftime("%Y-%m-%d")

    # Replace placeholders
    result = pattern.replace("today's date", today)
    result = result.replace("original name", name)
    result = result.replace("original extension", ext)

    # Parse natural language dates (e.g., "next Monday")
    if "next " in result or "last " in result:
        try:
            result = parse(result, fuzzy=True).strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Regex transformations (e.g., "uppercase", "lowercase", "title case")
    if "uppercase" in result:
        return name.upper() + ext
    elif "lowercase" in result:
        return name.lower() + ext.lower()
    elif "title case" in result:
        return name.title() + ext

    # Remove invalid characters
    result = re.sub(r'[\\/*?:"<>|]', "_", result)
    return result


if __name__ == "__main__":
    cli()