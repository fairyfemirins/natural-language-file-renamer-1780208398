#!/usr/bin/env python3
"""
Natural Language File Renamer (nlrename)
A CLI tool to batch-rename files using natural language commands.

Example:
  nlrename "today's date + original name" *.txt
  nlrename "lowercase + replace ' ' with '_'" *.jpg
"""

import os
import re
import sys
from datetime import datetime
from typing import List, Optional

import click
from dateutil.relativedelta import relativedelta


class NaturalLanguageParser:
    """Parse natural language commands into file renaming rules."""

    @staticmethod
    def parse_command(command: str) -> dict:
        """Convert natural language into a structured renaming rule."""
        rule = {
            "prefix": "",
            "suffix": "",
            "transforms": [],
            "date_format": None,
            "regex_replace": None,
        }

        # Date parsing
        if "today" in command:
            date_format = "%Y-%m-%d"
            rule["date_format"] = (datetime.now().strftime, date_format)
        elif "yesterday" in command:
            date_format = "%Y-%m-%d"
            rule["date_format"] = ((datetime.now() - relativedelta(days=1)).strftime, date_format)
        elif "tomorrow" in command:
            date_format = "%Y-%m-%d"
            rule["date_format"] = ((datetime.now() + relativedelta(days=1)).strftime, date_format)

        # Transformations
        if "lowercase" in command:
            rule["transforms"].append(str.lower)
        if "uppercase" in command:
            rule["transforms"].append(str.upper)
        if "titlecase" in command:
            rule["transforms"].append(str.title)

        # Regex replacements
        if "replace" in command:
            parts = re.search(r"replace ['\"](.*?)['\"] with ['\"](.*?)['\"]", command)
            if parts:
                rule["regex_replace"] = (parts.group(1), parts.group(2))

        # Prefix/suffix
        if "original name" in command:
            if rule["date_format"]:
                formatter, date_format = rule["date_format"]
                date_str = formatter(date_format)
                rule["prefix"] = date_str

        return rule

    @staticmethod
    def apply_rule(filename: str, rule: dict) -> str:
        """Apply the parsed rule to a filename."""
        name, ext = os.path.splitext(filename)
        new_name = name

        # Apply transforms
        for transform in rule["transforms"]:
            new_name = transform(new_name)

        # Apply regex replacement
        if rule["regex_replace"]:
            pattern, repl = rule["regex_replace"]
            new_name = re.sub(pattern, repl, new_name)

        # Apply date prefix if set
        if rule["date_format"] and not rule["prefix"]:
            formatter, date_format = rule["date_format"]
            date_str = formatter(date_format)
            new_name = f"{date_str}_{new_name}"
        else:
            new_name = f"{rule['prefix']}_{new_name}"

        new_name = f"{new_name}{rule['suffix']}".strip().lstrip("_")
        return f"{new_name}{ext}"


@click.command()
@click.argument("command", type=str)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.option("--dry-run", is_flag=True, help="Show what would be renamed without actually renaming.")
def cli(command: str, files: List[str], dry_run: bool) -> None:
    """Rename files using natural language commands."""
    if not files:
        click.echo("Error: No files provided.", err=True)
        sys.exit(1)

    rule = NaturalLanguageParser.parse_command(command)
    for file_path in files:
        dirname = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        new_name = NaturalLanguageParser.apply_rule(filename, rule)
        new_path = os.path.join(dirname, new_name)

        if dry_run:
            click.echo(f"DRY RUN: {filename} -> {new_name}")
        else:
            try:
                os.rename(file_path, new_path)
                click.echo(f"Renamed: {filename} -> {new_name}")
            except OSError as e:
                click.echo(f"Error renaming {filename}: {e}", err=True)


if __name__ == "__main__":
    cli()