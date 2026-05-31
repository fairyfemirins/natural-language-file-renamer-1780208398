import os
import sys
import tempfile

# Add the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from nl_renamer.parser import parse_pattern
from nl_renamer.transformer import rename_files


def test_parse_pattern():
    print("Testing parse_pattern...")
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    assert parse_pattern("today's date + original name", "file.txt") == f"{today}_file.txt"
    assert parse_pattern("lowercase", "FILE.TXT") == "file.txt"
    assert parse_pattern("uppercase", "file.txt") == "FILE.TXT"
    assert parse_pattern("replace 'file' with 'doc'", "file.txt") == "doc.txt"
    print("✅ parse_pattern tests passed")


def test_rename_files():
    print("Testing rename_files...")
    with tempfile.TemporaryDirectory() as tmp_dir:
        # Create test files
        file1 = os.path.join(tmp_dir, "file1.txt")
        with open(file1, "w") as f:
            f.write("test")
        file2 = os.path.join(tmp_dir, "file2.txt")
        with open(file2, "w") as f:
            f.write("test")
        
        # Test dry run
        results = rename_files([file1, file2], "lowercase", dry_run=True)
        assert "dry run" in results[0]
        assert "dry run" in results[1]
        assert os.path.exists(file1)
        assert os.path.exists(file2)
        
        # Test actual rename
        results = rename_files([file1, file2], "lowercase", dry_run=False)
        assert "✅" in results[0]
        assert "✅" in results[1]
        assert os.path.exists(os.path.join(tmp_dir, "file1.txt"))
        assert os.path.exists(os.path.join(tmp_dir, "file2.txt"))
    print("✅ rename_files tests passed")


if __name__ == "__main__":
    test_parse_pattern()
    test_rename_files()
    print("🎉 All tests passed!")