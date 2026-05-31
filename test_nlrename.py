#!/usr/bin/env python3
import os
import tempfile
import shutil
from nlrename import NaturalLanguageParser
from datetime import datetime

def test_natural_language_parser():
    """Test the NaturalLanguageParser with various commands."""
    test_cases = [
        {
            "command": "today's date + original name",
            "filename": "test.txt",
            "expected": f"{datetime.now().strftime('%Y-%m-%d')}_test.txt",
        },
        {
            "command": "lowercase + replace ' ' with '_'",
            "filename": "Test File.txt",
            "expected": "test_file.txt",
        },
        {
            "command": "uppercase + today's date",
            "filename": "test.txt",
            "expected": f"{datetime.now().strftime('%Y-%m-%d').upper()}_TEST.txt",
        },
    ]

    for case in test_cases:
        rule = NaturalLanguageParser.parse_command(case["command"])
        result = NaturalLanguageParser.apply_rule(case["filename"], rule)
        print(f"Command: {case['command']}")
        print(f"Rule: {rule}")
        print(f"Result: {result}")
        print(f"Expected: {case['expected']}")
        assert result == case["expected"], f"Failed: {case['command']} -> {result} (expected {case['expected']})"
        print(f"✓ {case['command']} -> {result}")

if __name__ == "__main__":
    test_natural_language_parser()