#!/usr/bin/env python3
"""Unit tests for nlrename.py"""

import os
import tempfile
import unittest
from datetime import datetime
from nlrename import parse_expression


class TestNaturalLanguageFileRenamer(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test.txt")
        with open(self.test_file, 'w') as f:
            f.write("test")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_todays_date(self) -> None:
        today = datetime.now().strftime("%Y-%m-%d")
        result = parse_expression("today's date original name", "test", ".txt")
        self.assertEqual(result, f"{today} test.txt")

    def test_lowercase(self) -> None:
        result = parse_expression("lowercase", "TEST", ".txt")
        self.assertEqual(result, "test.txt")

    def test_regex(self) -> None:
        result = parse_expression("regex:test->demo", "test", ".txt")
        self.assertEqual(result, "demo.txt")


if __name__ == '__main__':
    unittest.main()