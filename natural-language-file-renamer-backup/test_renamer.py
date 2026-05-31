#!/usr/bin/env python3
import os
import re
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

if __name__ == "__main__":
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_files = {
            "test1.PDF": os.path.join(tmpdir, "test1.PDF"),
            "test2.pdf": os.path.join(tmpdir, "test2.pdf"),
            "draft.txt": os.path.join(tmpdir, "draft.txt"),
        }
        for name, path in test_files.items():
            with open(path, "w") as f:
                f.write("test")

        # Test 1: "all PDFs to lowercase"
        assert apply_pattern("test1.PDF", "all pdfs to lowercase", test_files["test1.PDF"]) == "test1.pdf"
        assert apply_pattern("test2.pdf", "all pdfs to lowercase", test_files["test2.pdf"]) == "test2.pdf"

        # Test 2: "replace 'draft' with 'final'"
        assert apply_pattern("draft.txt", "replace 'draft' with 'final'", test_files["draft.txt"]) == "final.txt"

        # Test 3: "prepend '2026-' to files modified today"
        os.utime(test_files["test1.PDF"], (os.path.getatime(test_files["test1.PDF"]), os.path.getmtime(test_files["test1.PDF"])))
        assert apply_pattern("test1.PDF", "prepend '2026-' to files modified today", test_files["test1.PDF"]) == "2026-test1.PDF"

    print("All tests passed!")