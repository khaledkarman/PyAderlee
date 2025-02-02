"""
Tests for PyAderlee FileSystem class
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>
"""

import unittest
import os
import json
from pathlib import Path
from PyAderlee import FileSystem

class TestFileSystem(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.test_dir = Path("test_data")
        self.test_dir.mkdir(exist_ok=True)
        self.fs = FileSystem(self.test_dir)
        self.test_data = {"name": "John", "age": 30}
        self.test_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]

    def tearDown(self):
        """Clean up test environment"""
        for file in self.test_dir.glob("*"):
            file.unlink()
        self.test_dir.rmdir()

    def test_write_read_file(self):
        """Test basic file writing and reading"""
        test_content = "Hello, World!"
        self.fs.write_file("test.txt", test_content)
        content = self.fs.read_file("test.txt")
        self.assertEqual(content, test_content)

    def test_write_read_json(self):
        """Test JSON file writing and reading"""
        self.fs.write_json("test.json", self.test_data)
        data = self.fs.read_json("test.json")
        self.assertEqual(data, self.test_data)

    def test_write_read_csv(self):
        """Test CSV file writing and reading"""
        self.fs.write_csv("test.csv", self.test_list)
        data = self.fs.read_csv("test.csv")
        self.assertEqual(len(data), len(self.test_list))
        self.assertEqual(data[0]["name"], self.test_list[0]["name"])
        self.assertEqual(data[1]["age"], self.test_list[1]["age"])

    def test_list_files(self):
        """Test file listing"""
        self.fs.write_file("test1.txt", "content")
        self.fs.write_file("test2.txt", "content")
        files = self.fs.list_files("*.txt")
        self.assertEqual(len(list(files)), 2)

    def test_exists(self):
        """Test file existence check"""
        self.fs.write_file("test.txt", "content")
        self.assertTrue(self.fs.exists("test.txt"))
        self.assertFalse(self.fs.exists("nonexistent.txt"))

if __name__ == '__main__':
    unittest.main() 