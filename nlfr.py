#!/usr/bin/env python3
"""
Natural Language File Renamer (nlfr)

A CLI tool to rename files using natural language expressions.
Examples:
  nlfr "today's date + original name" file.txt
  nlfr "lowercase + uuid" image.JPG
  nlfr "parent folder name + counter" *.md

Supported expressions:
  - today's date, yesterday's date, tomorrow's date
  - original name, original extension
  - uuid, counter
  - lowercase, uppercase, titlecase
  - parent folder name
  - custom text (e.g., "notes_")
"""

import os
import re
import uuid
from datetime import datetime, timedelta
import click
from dateutil.relativedelta import relativedelta


def parse_expression(expr, original_name, original_ext, parent_folder, counter):
    """Parse natural language expression and return the new filename."""
    # Replace placeholders
    expr = expr.replace("original name", original_name)
    expr = expr.replace("original extension", original_ext)
    expr = expr.replace("parent folder name", parent_folder)
    expr = expr.replace("uuid", str(uuid.uuid4()))
    expr = expr.replace("counter", str(counter))

    # Date expressions
    today = datetime.now()
    date_expressions = {
        "today's date": today.strftime("%Y-%m-%d"),
        "yesterday's date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
        "tomorrow's date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
        "this month": today.strftime("%Y-%m"),
        "last month": (today - relativedelta(months=1)).strftime("%Y-%m"),
        "next month": (today + relativedelta(months=1)).strftime("%Y-%m"),
    }
    for key, value in date_expressions.items():
        expr = expr.replace(key, value)

    # Case transformations
    if "lowercase" in expr:
        expr = expr.replace("lowercase", "").lower()
    if "uppercase" in expr:
        expr = expr.replace("uppercase", "").upper()
    if "titlecase" in expr:
        expr = expr.replace("titlecase", "").title()

    # Remove extra whitespace and trim
    expr = re.sub(r'\s+', ' ', expr).strip()
    return expr


@click.command()
@click.argument('expression', type=str)
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.option('--dry-run', is_flag=True, help="Show what would be renamed without actually renaming.")
@click.option('--counter-start', type=int, default=1, help="Starting value for the counter (default: 1).")
def cli(expression, files, dry_run, counter_start):
    """Rename files using natural language expressions."""
    if not files:
        click.echo("Error: No files provided.", err=True)
        return

    for idx, file_path in enumerate(files, start=counter_start):
        original_name = os.path.splitext(os.path.basename(file_path))[0]
        original_ext = os.path.splitext(file_path)[1][1:]  # Remove leading dot
        parent_folder = os.path.basename(os.path.dirname(os.path.abspath(file_path)))
        new_name = parse_expression(expression, original_name, original_ext, parent_folder, idx)
        new_name = re.sub(r'[\\/*?:"<>|]', '_', new_name)  # Sanitize for filesystem
        new_path = os.path.join(os.path.dirname(file_path), f"{new_name}.{original_ext}")

        if dry_run:
            click.echo(f"DRY RUN: {file_path} -> {new_path}")
        else:
            try:
                os.rename(file_path, new_path)
                click.echo(f"Renamed: {file_path} -> {new_path}")
            except Exception as e:
                click.echo(f"Error renaming {file_path}: {e}", err=True)


if __name__ == "__main__":
    cli()