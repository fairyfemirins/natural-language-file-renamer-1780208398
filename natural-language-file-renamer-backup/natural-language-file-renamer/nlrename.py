#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)

A CLI tool to rename files using natural language expressions.
Examples:
  nlrename "today's date + original name" file.txt
  nlrename "lowercase + .bak" FILE.TXT
"""

import os
import re
import click
from datetime import datetime
from dateutil.relativedelta import relativedelta


@click.command()
@click.argument('expression', type=str)
@click.argument('files', type=click.Path(exists=True), nargs=-1)
@click.option('--dry-run', is_flag=True, help='Show what would be renamed without actually doing it.')
def cli(expression: str, files: list, dry_run: bool) -> None:
    """Rename files using natural language expressions."""
    for file_path in files:
        dirname, basename = os.path.split(file_path)
        name, ext = os.path.splitext(basename)
        
        # Parse expression
        new_name = parse_expression(expression, name, ext)
        new_path = os.path.join(dirname, new_name)
        
        if dry_run:
            click.echo(f"DRY RUN: {file_path} -> {new_path}")
        else:
            try:
                os.rename(file_path, new_path)
                click.echo(f"Renamed: {file_path} -> {new_path}")
            except OSError as e:
                click.echo(f"Error renaming {file_path}: {e}", err=True)


def parse_expression(expression: str, original_name: str, ext: str) -> str:
    """Parse natural language expression into a new filename."""
    # Replace placeholders
    expr = expression.replace("original name", original_name)
    
    # Date transformations
    if "today's date" in expr:
        today = datetime.now().strftime("%Y-%m-%d")
        expr = expr.replace("today's date", today)
    if "tomorrow's date" in expr:
        tomorrow = (datetime.now() + relativedelta(days=1)).strftime("%Y-%m-%d")
        expr = expr.replace("tomorrow's date", tomorrow)
    
    # Case transformations
    if "lowercase" in expr:
        expr = expr.replace("lowercase", original_name.lower())
    if "uppercase" in expr:
        expr = expr.replace("uppercase", original_name.upper())
    if "titlecase" in expr:
        expr = expr.replace("titlecase", original_name.title())
    
    # Regex transformations
    if "regex:" in expr:
        pattern, repl = expr.split("regex:")[1].split("->")
        expr = re.sub(pattern.strip(), repl.strip(), original_name)
    
    # Remove expression keywords and extra spaces
    expr = re.sub(r'\b(today\'s date|tomorrow\'s date|lowercase|uppercase|titlecase|\+)\b', '', expr)
    expr = re.sub(r'\s+', ' ', expr).strip()
    
    # Combine with extension
    return f"{expr}{ext}"


if __name__ == '__main__':
    cli()