#!/usr/bin/env python3
"""
Core logic for renaming files based on parsed commands.
"""

import os
import fnmatch
import re
from datetime import datetime
from typing import List, Optional
from .parser import parse_command, apply_transform


def rename_files(directory: str, command: str, dry_run: bool = False) -> List[str]:
    """
    Rename files in directory based on natural language command.
    
    Args:
        directory: Path to directory containing files to rename.
        command: Natural language command (e.g., "all PDFs to lowercase").
        dry_run: If True, return list of changes without applying them.
        
    Returns:
        List of changes (e.g., ["old.txt -> new.txt"]).
    """
    parsed = parse_command(command)
    changes = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue
        
        # Check file pattern (e.g., "*.pdf") with case-insensitive matching
        if not fnmatch.fnmatch(filename.lower(), parsed["pattern"].lower()):
            continue
        
        # Check date conditions (e.g., "older than 30 days")
        file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
        if parsed["older_than"] and file_mtime > parsed["older_than"]:
            continue
        if parsed["newer_than"] and file_mtime < parsed["newer_than"]:
            continue
        
        # Apply transform
        new_filename = filename
        if parsed["regex_replace"]:
            pattern, repl = parsed["regex_replace"]
            new_filename = re.sub(pattern, repl, new_filename)
        if parsed["transform"]:
            new_filename = apply_transform(new_filename, parsed["transform"], parsed["date_format"])
        
        if new_filename != filename:
            if dry_run:
                changes.append(f"{filename} -> {new_filename}")
            else:
                os.rename(filepath, os.path.join(directory, new_filename))
                changes.append(f"{filename} -> {new_filename}")
    
    return changes