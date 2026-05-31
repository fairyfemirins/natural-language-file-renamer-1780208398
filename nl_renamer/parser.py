"""
Natural language parser for file renaming patterns.

Supported patterns:
- "today's date + original name" -> "2026-05-31_original_name.txt"
- "lowercase" -> "original_name.txt"
- "uppercase" -> "ORIGINAL_NAME.TXT"
- "replace 'old' with 'new'" -> "new_name.txt"
"""

import re
from datetime import datetime
from dateutil.relativedelta import relativedelta


def parse_pattern(pattern: str, original_name: str) -> str:
    """Parse a natural language pattern and return the new filename."""
    name_without_ext, ext = _split_extension(original_name)
    
    # Handle date patterns
    if "today's date" in pattern:
        today = datetime.now().strftime("%Y-%m-%d")
        pattern = pattern.replace("today's date", today)
    if "tomorrow's date" in pattern:
        tomorrow = (datetime.now() + relativedelta(days=1)).strftime("%Y-%m-%d")
        pattern = pattern.replace("tomorrow's date", tomorrow)
    if "yesterday's date" in pattern:
        yesterday = (datetime.now() + relativedelta(days=-1)).strftime("%Y-%m-%d")
        pattern = pattern.replace("yesterday's date", yesterday)
    
    # Handle original name
    if "original name" in pattern:
        pattern = pattern.replace("original name", name_without_ext)
    
    # Handle standalone case transformations
    if pattern.strip() == "lowercase":
        return f"{name_without_ext.lower()}{ext.lower()}"
    if pattern.strip() == "uppercase":
        return f"{name_without_ext.upper()}{ext.upper()}"

    # Handle case transformations in patterns
    if "lowercase" in pattern:
        name_without_ext = name_without_ext.lower()
        pattern = pattern.replace("lowercase", "")
    if "uppercase" in pattern:
        name_without_ext = name_without_ext.upper()
        pattern = pattern.replace("uppercase", "")
    
    # Handle replacements
    replacement_match = re.search(r"replace ['\"](.*?)['\"] with ['\"](.*?)['\"]", pattern)
    if replacement_match:
        old, new = replacement_match.groups()
        name_without_ext = name_without_ext.replace(old, new)
        pattern = pattern.replace(f"replace '{old}' with '{new}'", "")
        pattern = pattern.replace(f"replace \"{old}\" with \"{new}\"", "")
        pattern = name_without_ext  # Ensure the name is preserved
    
    # Clean up leftover keywords
    pattern = pattern.replace("+", "_").replace(" ", "_")
    pattern = re.sub(r"_+", "_", pattern).strip("_")
    
    return f"{pattern}{ext}"


def _split_extension(filename: str) -> tuple[str, str]:
    """Split filename into name and extension."""
    if "." not in filename:
        return filename, ""
    name, ext = filename.rsplit(".", 1)
    return name, f".{ext}"