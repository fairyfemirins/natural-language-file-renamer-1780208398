#!/usr/bin/env python3
import os
import re
import click
from datetime import datetime
from dateutil.parser import parse

@click.command()
@click.argument("instruction", type=str)
@click.argument("path", type=click.Path(exists=True), default=".")
@click.option("--dry-run", is_flag=True, help="Preview changes without renaming.")
@click.option("--verbose", is_flag=True, help="Show debug output.")
def cli(instruction, path, dry_run, verbose):
    """Rename files using natural language instructions."""
    if verbose:
        click.echo(f"DEBUG: Instruction: {instruction}")
        click.echo(f"DEBUG: Path: {path}")

    # Parse instruction
    patterns = {
        "lowercase": r"(all|every|convert|change).*\b(lowercase|lower case|lower-case)\b",
        "uppercase": r"(all|every|convert|change).*\b(uppercase|upper case|upper-case)\b",
        "add_date": r"(add|append|prepend).*\b(today|date)\b",
        "replace": r"replace\s+['\"](.*?)['\"]\s+with\s+['\"](.*?)['\"]",
    }

    for action, pattern in patterns.items():
        match = re.search(pattern, instruction, re.IGNORECASE)
        if match:
            if action == "lowercase":
                rename_files(path, lambda name, ext: (name.lower(), ext.lower()), dry_run, verbose)
            elif action == "uppercase":
                rename_files(path, lambda name, ext: (name.upper(), ext.upper()), dry_run, verbose)
            elif action == "add_date":
                today = datetime.now().strftime("%Y-%m-%d")
                rename_files(path, lambda name, ext: (f"{today}_{name}", ext), dry_run, verbose)
            elif action == "replace":
                old, new = match.groups()
                rename_files(path, lambda name, ext: (name.replace(old, new), ext), dry_run, verbose)
            break
    else:
        click.echo("Error: Could not parse instruction. Examples:")
        click.echo("  nlrename \"all PDFs to lowercase\" .")
        click.echo("  nlrename \"add today's date to all files\" .")
        click.echo("  nlrename \"replace 'draft' with 'final'\" .")

def rename_files(path, transform, dry_run, verbose):
    for filename in os.listdir(path):
        if filename.startswith("."):
            continue
        name, ext = os.path.splitext(filename)
        new_name, new_ext = transform(name, ext)
        new_filename = f"{new_name}{new_ext}"
        if filename != new_filename:
            if verbose:
                click.echo(f"DEBUG: Renaming {filename} -> {new_filename}")
            if dry_run:
                click.echo(f"[DRY RUN] Would rename: {filename} -> {new_filename}")
            else:
                os.rename(
                    os.path.join(path, filename),
                    os.path.join(path, new_filename),
                )
                click.echo(f"Renamed: {filename} -> {new_filename}")

if __name__ == "__main__":
    cli()