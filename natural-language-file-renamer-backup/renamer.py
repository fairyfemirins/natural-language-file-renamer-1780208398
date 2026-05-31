#!/usr/bin/env python3
import os
import re
import click
from datetime import datetime
from dateutil.parser import parse
from typing import List, Optional

def apply_pattern(filename: str, pattern: str, file_path: str) -> str:
    """Apply natural language pattern to filename."""
    # Pattern 1: "all X to lowercase/uppercase"
    if match := re.match(r"all (.*?)s to (lowercase|uppercase)", pattern, re.IGNORECASE):
        ext = match.group(1)
        case = match.group(2).lower()
        if filename.lower().endswith(f".{ext.lower()}"):
            name, ext_part = os.path.splitext(filename)
            return f"{name.lower() if case == 'lowercase' else name.upper()}{ext_part.lower() if case == 'lowercase' else ext_part.upper()}"

    # Pattern 2: "prepend X to files modified Y"
    elif match := re.match(r"prepend '(.+?)' to files modified (.+)", pattern, re.IGNORECASE):
        prefix = match.group(1)
        time_desc = match.group(2)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        today = datetime.now().date()

        if time_desc == "today" and file_mtime.date() == today:
            return f"{prefix}{filename}"
        elif time_desc == "this week" and (today - file_mtime.date()).days <= 7:
            return f"{prefix}{filename}"

    # Pattern 3: "replace X with Y"
    elif match := re.match(r"replace '(.+?)' with '(.+?)'", pattern, re.IGNORECASE):
        old_str, new_str = match.group(1), match.group(2)
        return filename.replace(old_str, new_str)

    # Pattern 4: "add date to files modified today"
    elif "add date" in pattern.lower() and "today" in pattern.lower():
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        today = datetime.now().date()
        if file_mtime.date() == today:
            date_str = datetime.now().strftime("%Y-%m-%d")
            name, ext = os.path.splitext(filename)
            return f"{name}_{date_str}{ext}"

    return filename

@click.command()
@click.argument("pattern", type=str)
@click.argument("files", type=click.Path(exists=True), nargs=-1)
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without making changes.")
@click.option("--verbose", is_flag=True, help="Print detailed output.")
def rename_files(pattern: str, files: List[str], dry_run: bool, verbose: bool):
    """
    Rename files using natural language patterns.

    Examples:
        rename "all pdfs to lowercase" *.pdf
        rename "prepend '2026-' to files modified today" *
        rename "replace 'draft' with 'final'" *.txt
    """
    if not files:
        raise click.UsageError("No files provided.")

    for file_path in files:
        if not os.path.isfile(file_path):
            continue

        dir_name, old_name = os.path.split(file_path)
        new_name = apply_pattern(old_name, pattern, file_path)

        if new_name != old_name:
            new_path = os.path.join(dir_name, new_name)
            if verbose or dry_run:
                click.echo(f"{old_name} -> {new_name}")
            if not dry_run:
                os.rename(file_path, new_path)

if __name__ == "__main__":
    rename_files()