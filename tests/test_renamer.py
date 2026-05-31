import os
import pytest
from nl_renamer.parser import parse_pattern
from nl_renamer.transformer import rename_files


def test_parse_pattern():
    assert parse_pattern("today's date + original name", "file.txt") == f"{os.date().strftime('%Y-%m-%d')}_file.txt"
    assert parse_pattern("lowercase", "FILE.TXT") == "file.txt"
    assert parse_pattern("uppercase", "file.txt") == "FILE.TXT"
    assert parse_pattern("replace 'file' with 'doc'", "file.txt") == "doc.txt"


def test_rename_files(tmp_path):
    # Create test files
    file1 = tmp_path / "file1.txt"
    file1.write_text("test")
    file2 = tmp_path / "file2.txt"
    file2.write_text("test")
    
    # Test dry run
    results = rename_files([str(file1), str(file2)], "lowercase", dry_run=True)
    assert "dry run" in results[0]
    assert "dry run" in results[1]
    assert file1.exists()
    assert file2.exists()
    
    # Test actual rename
    results = rename_files([str(file1), str(file2)], "lowercase", dry_run=False)
    assert "✅" in results[0]
    assert "✅" in results[1]
    assert (tmp_path / "file1.txt").exists()
    assert (tmp_path / "file2.txt").exists()