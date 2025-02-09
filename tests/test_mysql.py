"""
Tests for PyAderlee MySQLManager class
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>
"""

import unittest
from unittest.mock import patch, MagicMock
from PyAderlee import MySQLManager

class TestMySQLManager(unittest.TestCase):
    """Test suite for MySQLManager class"""

    def setUp(self):
        """Set up test environment with mocked MySQL connection"""
        self.patcher = patch('mysql.connector.connect')
        self.mock_connect = self.patcher.start()
        
        # Mock cursor and connection
        self.mock_cursor = MagicMock()
        self.mock_connection = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor
        self.mock_connect.return_value = self.mock_connection
        
        # Initialize MySQLManager with test config
        self.db = MySQLManager(
            host="localhost",
            user="test_user",
            password="test_pass",
            database="test_db"
        )
        self.db.connect()

    def tearDown(self):
        """Clean up test environment"""
        self.patcher.stop()
        if self.db:
            self.db.disconnect()

    def test_connection(self):
        """Test database connection"""
        self.mock_connect.assert_called_once()
        self.assertIsNotNone(self.db.connection)
        self.assertIsNotNone(self.db.cursor)

    def test_insert(self):
        """Test data insertion"""
        test_data = {"name": "John", "age": 30}
        self.mock_cursor.lastrowid = 1
        
        last_id = self.db.insert("users", test_data)
        
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(last_id, 1)

    def test_select(self):
        """Test data selection"""
        expected_result = [
            {"id": 1, "name": "John", "age": 30},
            {"id": 2, "name": "Jane", "age": 25}
        ]
        self.mock_cursor.fetchall.return_value = expected_result
        
        result = self.db.select("users", ["name", "age"], {"age": 30})
        
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(result, expected_result)

    def test_update(self):
        """Test data update"""
        self.mock_cursor.rowcount = 1
        
        rows_affected = self.db.update(
            "users",
            {"age": 31},
            {"name": "John"}
        )
        
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(rows_affected, 1)

    def test_delete(self):
        """Test data deletion"""
        self.mock_cursor.rowcount = 1
        
        rows_affected = self.db.delete("users", {"name": "John"})
        
        self.mock_cursor.execute.assert_called_once()
        self.assertEqual(rows_affected, 1)

    def test_execute_select(self):
        """Test execute method with SELECT query"""
        expected_result = [{"id": 1, "name": "John"}]
        self.mock_cursor.fetchall.return_value = expected_result
        
        result = self.db.execute("SELECT * FROM users WHERE id = %s", (1,))
        
        self.assertEqual(result, expected_result)

    def test_execute_insert(self):
        """Test execute method with INSERT query"""
        result = self.db.execute(
            "INSERT INTO users (name, age) VALUES (%s, %s)",
            ("John", 30)
        )
        
        self.mock_cursor.execute.assert_called_once()
        self.assertIsNone(result)

    def test_context_manager(self):
        """Test context manager functionality"""
        with MySQLManager(
            host="localhost",
            user="test_user",
            password="test_pass",
            database="test_db"
        ) as db:
            self.assertIsNotNone(db.connection)
            self.assertIsNotNone(db.cursor)
        
        # Connection should be closed after context
        self.assertIsNone(db.connection)
        self.assertIsNone(db.cursor)

    def test_connection_error(self):
        """Test connection error handling"""
        self.mock_connect.side_effect = Exception("Connection failed")
        
        with self.assertRaises(Exception) as context:
            MySQLManager(
                host="invalid_host",
                user="test_user",
                password="test_pass",
                database="test_db"
            ).connect()
        
        self.assertTrue("Connection failed" in str(context.exception))

    def test_query_error(self):
        """Test query error handling"""
        self.mock_cursor.execute.side_effect = Exception("Query failed")
        
        with self.assertRaises(Exception) as context:
            self.db.execute("INVALID SQL")
        
        self.assertTrue("Query failed" in str(context.exception))

if __name__ == '__main__':
    unittest.main() 