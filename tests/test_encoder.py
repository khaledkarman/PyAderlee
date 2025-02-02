"""
Tests for PyAderlee Encoder class
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>
"""

import unittest
import json
from PyAderlee import Encoder

class TestEncoder(unittest.TestCase):
    def setUp(self):
        self.encoder = Encoder()
        self.test_dict = {"name": "John", "age": 30}
        self.test_list = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25}
        ]

    def test_to_json(self):
        """Test JSON encoding"""
        json_str = self.encoder.to_json(self.test_dict)
        self.assertEqual(json.loads(json_str), self.test_dict)

    def test_from_json(self):
        """Test JSON decoding"""
        json_str = json.dumps(self.test_dict)
        data = self.encoder.from_json(json_str)
        self.assertEqual(data, self.test_dict)

    def test_to_csv_empty(self):
        """Test CSV encoding with empty data"""
        csv_str = self.encoder.to_csv([])
        self.assertEqual(csv_str, "")

    def test_to_csv(self):
        """Test CSV encoding"""
        csv_str = self.encoder.to_csv(self.test_list)
        expected = "name,age\nJohn,30\nJane,25"
        self.assertEqual(csv_str.replace('\r', ''), expected)

if __name__ == '__main__':
    unittest.main() 