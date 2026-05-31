#!/usr/bin/env python3
"""
Natural Language File Renamer

A CLI tool to rename files using natural language instructions.
Examples:
  - "today's date + original name"
  - "lowercase and replace spaces with underscores"
  - "add prefix 'backup_'"
"""

import os
import re
import click
from datetime import datetime
from dateutil.parser import parse


def parse_instruction(instruction: str, original_name: str, original_ext: str) -> str:
    """Parse natural language instruction and return new filename (without extension)."""
    instruction = instruction.lower().strip()
    new_name = original_name
    
    # Handle dates
    if "today" in instruction:
        today = datetime.now().strftime("%Y-%m-%d")
        if "date + original" in instruction:
            new_name = f"{today}_{new_name}"
        elif "original + date" in instruction:
            new_name = f"{new_name}_{today}"
        else:
            new_name = today
    
    # Handle case transformations
    if "lowercase" in instruction:
        new_name = new_name.lower()
    if "uppercase" in instruction:
        new_name = new_name.upper()
    if "title case" in instruction:
        new_name = new_name.title()
    
    # Handle replacements
    if "replace spaces with underscores" in instruction:
        new_name = new_name.replace(" ", "_")
    if "replace underscores with spaces" in instruction:
        new_name = new_name.replace("_", " ")
    if "replace spaces with hyphens" in instruction:
        new_name = new_name.replace(" ", "-")
    if "replace hyphens with spaces" in instruction:
        new_name = new_name.replace("-", " ")
    
    # Handle prefixes/suffixes
    if "add prefix" in instruction:
        prefix = re.search(r"add prefix ['\"](.*?)['\"]", instruction)
        if prefix:
            new_name = f"{prefix.group(1)}{new_name}"
    if "add suffix" in instruction:
        suffix = re.search(r"add suffix ['\"](.*?)['\"]", instruction)
        if suffix:
            new_name = f"{new_name}{suffix.group(1)}"
    
    # Handle regex replacements
    if "replace " in instruction and " with " in instruction:
        parts = instruction.split("replace ")[1].split(" with ")
        if len(parts) == 2:
            old, new = parts
            new_name = new_name.replace(old.strip(), new.strip())
    
    return new_name


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--instruction", "-i", required=True, help="Natural language instruction for renaming.")
@click.option("--dry-run", is_flag=True, help="Preview changes without renaming.")

def cli(path, instruction, dry_run):
    """Rename a file using natural language instructions."""
    if not os.path.isfile(path):
        click.echo(f"Error: '{path}' is not a file.", err=True)
        return
    
    dir_name, file_name = os.path.split(path)
    original_name, original_ext = os.path.splitext(file_name)
    
    new_name = parse_instruction(instruction, original_name, original_ext)
    new_file_name = f"{new_name}{original_ext}"
    new_file_path = os.path.join(dir_name, new_file_name)
    
    if path == new_file_path:
        click.echo("No changes needed.")
        return
    
    if dry_run:
        click.echo(f"[DRY RUN] {path} -> {new_file_path}")
    else:
        try:
            os.rename(path, new_file_path)
            click.echo(f"Renamed: {path} -> {new_file_path}")
        except Exception as e:
            click.echo(f"Error renaming {path}: {e}", err=True)


if __name__ == "__main__":
    cli()