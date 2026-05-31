#!/usr/bin/env python3
"""
Natural language parser for file renaming commands.
"""

import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List, Optional, Tuple


def parse_command(command: str) -> Dict:
    """
    Parse natural language command into structured data.
    
    Examples:
        "all PDFs to lowercase" -> {"pattern": "*.pdf", "transform": "lowercase"}
        "files older than 30 days to archive_<date>" -> {"pattern": "*", "transform": "archive_<date>", "older_than": 30}
    """
    command = command.lower().strip()
    result = {
        "pattern": "*",
        "transform": None,
        "older_than": None,
        "newer_than": None,
        "date_format": None,
        "regex_replace": None,
    }
    
    # Extract file pattern (e.g., "all PDFs", "*.txt files")
    pattern_match = re.search(r"(all|every|\*)\s+([a-z0-9.*]+)", command)
    if pattern_match:
        result["pattern"] = pattern_match.group(2).replace(" ", "")
        if "." not in result["pattern"]:
            result["pattern"] = f"*.{result['pattern'].rstrip('s')}"
    
    # Extract transform (e.g., "to lowercase", "to archive_<date>")
    transform_match = re.search(r"to\s+([a-z0-9_<>]+)", command)
    if transform_match:
        result["transform"] = transform_match.group(1)
    
    # Extract date-based conditions (e.g., "older than 30 days")
    date_match = re.search(r"(older|newer)\s+than\s+(\d+)\s+(day|week|month|year)s?", command)
    if date_match:
        age = int(date_match.group(2))
        unit = date_match.group(3)
        delta = {unit: age}
        if date_match.group(1) == "older":
            result["older_than"] = datetime.now() - relativedelta(**delta)
        else:
            result["newer_than"] = datetime.now() - relativedelta(**delta)
    
    # Extract date format (e.g., "<date:YYYYMMDD>")
    date_format_match = re.search(r"<date:([^>]+)>", command)
    if date_format_match:
        result["date_format"] = date_format_match.group(1)
    
    # Extract regex replace (e.g., "replace 'foo' with 'bar'")
    regex_match = re.search(r"replace\s+'([^']+)'\s+with\s+'([^']+)'", command)
    if regex_match:
        result["regex_replace"] = (regex_match.group(1), regex_match.group(2))
    
    return result


def apply_transform(filename: str, transform: str, date_format: Optional[str] = None) -> str:
    """
    Apply transform to filename.
    """
    if transform == "lowercase":
        return filename.lower()
    elif transform == "uppercase":
        return filename.upper()
    elif transform == "titlecase":
        return filename.title()
    elif transform.startswith("archive_"):
        date_str = datetime.now().strftime(date_format or "%Y%m%d")
        return f"{transform.replace('<date>', date_str)}_{filename}"
    else:
        return filename