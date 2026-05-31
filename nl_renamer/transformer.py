"""
File renaming logic.
"""

import os
from typing import List


def rename_files(files: List[str], pattern: str, dry_run: bool = False) -> List[str]:
    """Rename files using a natural language pattern."""
    from nl_renamer.parser import parse_pattern
    
    results = []
    for file_path in files:
        if not os.path.exists(file_path):
            results.append(f"❌ {file_path}: File not found")
            continue
        
        dir_name, original_name = os.path.split(file_path)
        new_name = parse_pattern(pattern, original_name)
        new_path = os.path.join(dir_name, new_name)
        
        if dry_run:
            results.append(f"🔍 {file_path} -> {new_path} (dry run)")
        else:
            try:
                os.rename(file_path, new_path)
                results.append(f"✅ {file_path} -> {new_path}")
            except Exception as e:
                results.append(f"❌ {file_path}: {str(e)}")
    
    return results