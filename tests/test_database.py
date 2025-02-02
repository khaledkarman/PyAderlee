"""
Tests for PyAderlee DatabaseManager class
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

This module contains unit tests for the DatabaseManager class,
covering all major functionality including:
- Basic CRUD operations
- Table management
- Schema inspection
- Connection handling
"""

import unittest
import os
from pathlib import Path
from PyAderlee import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """
    Test suite for DatabaseManager class.
    Tests all major database operations and ensures proper cleanup.
    """

    def setUp(self):
        """
        Set up test environment before each test.
        Creates a test database and initializes test table.
        """
        self.db_path = Path("test.db")
        self.db = DatabaseManager(self.db_path)
        self.db.connect()
        
        # Create test table
        self.db.create_table("test_table", {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "age": "INTEGER"
        })
    
    def tearDown(self):
        """Clean up test environment"""
        self.db.disconnect()
        if self.db_path.exists():
            os.remove(self.db_path)
    
    def test_insert_and_select(self):
        """
        Test data insertion and selection operations.
        Verifies that:
        - Data can be inserted correctly
        - Selected data matches inserted data
        - Column selection works properly
        """
        test_data = {"name": "John", "age": 30}
        self.db.insert("test_table", test_data)
        
        results = self.db.select("test_table", ["name", "age"])
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "John")
        self.assertEqual(results[0][1], 30)
    
    def test_update(self):
        """Test data update"""
        self.db.insert("test_table", {"name": "John", "age": 30})
        self.db.update("test_table", 
                      {"age": 31}, 
                      {"name": "John"})
        
        results = self.db.select("test_table", where={"name": "John"})
        self.assertEqual(results[0][2], 31)
    
    def test_delete(self):
        """Test data deletion"""
        self.db.insert("test_table", {"name": "John", "age": 30})
        self.db.delete("test_table", {"name": "John"})
        
        results = self.db.select("test_table")
        self.assertEqual(len(results), 0)
    
    def test_context_manager(self):
        """Test context manager functionality"""
        with DatabaseManager(self.db_path) as db:
            db.insert("test_table", {"name": "John", "age": 30})
            results = db.select("test_table")
            self.assertEqual(len(results), 1)

if __name__ == '__main__':
    unittest.main() 