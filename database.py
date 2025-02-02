"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

Database management module for PyAderlee.
This module provides a high-level interface for SQLite database operations
with support for table management, CRUD operations, and schema inspection.
"""

import sqlite3
from typing import List, Dict, Any, Union, Optional
from pathlib import Path

class DatabaseManager:
    """
    A class to handle SQLite database operations with built-in support for
    common database management tasks.

    Features:
    - CRUD operations (Create, Read, Update, Delete)
    - Table management (create, drop)
    - Schema inspection (tables, columns, indexes)
    - Foreign key and trigger management
    - Context manager support for automatic connection handling
    """
    def __init__(self, db_path: Union[str, Path]):
        """
        Initialize database manager with a path to SQLite database.
        Creates the database file if it doesn't exist.

        Args:
            db_path: Path to SQLite database file (str or Path object)
        """
        self.db_path = Path(db_path)
        self.connection = None
        self.cursor = None
    
    def connect(self) -> None:
        """
        Establish a connection to the SQLite database.
        Creates the database file if it doesn't exist.
        Sets up both connection and cursor objects.
        """
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
    
    def disconnect(self) -> None:
        """
        Close the database connection and cleanup resources.
        Safely handles disconnection even if connection wasn't established.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def execute(self, query: str, params: tuple = ()) -> Optional[List[tuple]]:
        """
        Execute an SQL query with optional parameters.
        Automatically handles connection and transaction management.

        Args:
            query: SQL query string to execute
            params: Query parameters for parameterized queries

        Returns:
            List of results for SELECT queries, None for other queries

        Example:
            >>> db.execute("SELECT * FROM users WHERE age > ?", (25,))
            [(1, "John", 30), (2, "Jane", 28)]
        """
        if not self.connection:
            self.connect()
            
        self.cursor.execute(query, params)
        
        if query.strip().upper().startswith('SELECT'):
            return self.cursor.fetchall()
        else:
            self.connection.commit()
            return None
    
    def insert(self, table_name: str, data: Dict[str, Any]) -> None:
        """
        Insert a single row of data into the specified table.

        Args:
            table_name: Name of the target table
            data: Dictionary mapping column names to their values

        Example:
            >>> db.insert("users", {"name": "John", "age": 30})
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute(query, tuple(data.values()))
    
    def select(self, table_name: str, columns: List[str] = None, 
               where: Dict[str, Any] = None) -> List[tuple]:
        """
        Select data from the specified table with optional column and condition filters.

        Args:
            table_name: Name of the target table
            columns: List of column names to select (None for all columns)
            where: Dictionary of column-value pairs for WHERE clause filtering
            
        Returns:
            List of tuples containing the query results

        Example:
            >>> db.select("users", ["name", "age"], {"age": 30})
            [("John", 30), ("Jane", 30)]
        """
        cols = '*' if not columns else ', '.join(columns)
        query = f"SELECT {cols} FROM {table_name}"
        
        if where:
            conditions = ' AND '.join([f"{k} = ?" for k in where.keys()])
            query += f" WHERE {conditions}"
            return self.execute(query, tuple(where.values()))
        
        return self.execute(query)
    
    def update(self, table_name: str, data: Dict[str, Any], 
               where: Dict[str, Any]) -> None:
        """
        Update existing records in the specified table.

        Args:
            table_name: Name of the target table
            data: Dictionary of column names and their new values
            where: Dictionary of column-value pairs for WHERE clause

        Example:
            >>> db.update("users", {"age": 31}, {"name": "John"})
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(where.values()))
        
        self.execute(query, params)
    
    def delete(self, table_name: str, where: Dict[str, Any]) -> None:
        """
        Delete records from the specified table that match the conditions.

        Args:
            table_name: Name of the target table
            where: Dictionary of column-value pairs for WHERE clause

        Example:
            >>> db.delete("users", {"name": "John"})
        """
        conditions = ' AND '.join([f"{k} = ?" for k in where.keys()])
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        
        self.execute(query, tuple(where.values()))
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """
        Create a new table with the specified columns.
        Uses STRICT mode for better type enforcement.

        Args:
            table_name: Name of the new table
            columns: Dictionary mapping column names to their SQL types

        Example:
            >>> db.create_table("users", {
            ...     "id": "INTEGER PRIMARY KEY",
            ...     "name": "TEXT NOT NULL",
            ...     "age": "INTEGER"
            ... })
        """
        cols = [f"{name} {dtype}" for name, dtype in columns.items()]
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)}) STRICT"
        self.execute(query)
    
    def show_tables(self) -> List[str]:
        """
        List all tables in the current database.

        Returns:
            List of table names

        Example:
            >>> db.show_tables()
            [("users",), ("products",)]
        """
        return self.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    def show_columns(self, table_name: str) -> List[str]:
        """
        Show all columns and their definitions for the specified table.

        Args:
            table_name: Name of the target table

        Returns:
            List of column definitions

        Example:
            >>> db.show_columns("users")
            [("id", "INTEGER", 1, 1), ("name", "TEXT", 1, 0)]
        """
        # return self.execute(f"PRAGMA table_info({table_name})")
        return self.execute(f"SELECT sql FROM sqlite_schema ")
        # return self.execute(f"SELECT name FROM PRAGMA_TABLE_INFO()")
    
    def show_table_schema(self, table_name: str) -> List[str]:
        """
        Get the complete SQL schema definition for the specified table.

        Args:
            table_name: Name of the target table

        Returns:
            SQL CREATE statement for the table

        Example:
            >>> db.show_table_schema("users")
            "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
        """
        # return self.execute(f"PRAGMA table_info({table_name})")
        ret = self.execute(f"SELECT sql FROM sqlite_schema WHERE name='{table_name}'")
        return ret[0][0]
    

    def show_table_structure(self, table_name: str) -> List[str]:
        """
        Get detailed information about table structure including columns,
        types, and constraints.

        Args:
            table_name: Name of the target table

        Returns:
            List of tuples containing column information
        """
        return self.execute(f"PRAGMA table_info({table_name})")
    
    def show_table_indexes(self, table_name: str) -> List[str]:
        """
        List all indexes defined for the specified table.

        Args:
            table_name: Name of the target table

        Returns:
            List of index definitions
        """
        return self.execute(f"PRAGMA index_list({table_name})")
    
    def show_table_index_info(self, table_name: str, index_name: str) -> List[str]:
        """Show table index info"""
        return self.execute(f"PRAGMA index_info({table_name})")

    def show_table_statistics(self, table_name: str) -> List[str]:
        """Show table statistics"""
        return self.execute(f"PRAGMA stats({table_name})")
    
    def show_table_triggers(self, table_name: str) -> List[str]:
        """Show table triggers"""
        return self.execute(f"PRAGMA trigger_list({table_name})")
    
    def show_table_trigger_info(self, table_name: str, trigger_name: str) -> List[str]:
        """Show table trigger info"""
        return self.execute(f"PRAGMA trigger_info({table_name})")

    def show_table_foreign_keys(self, table_name: str) -> List[str]:
        """
        List all foreign key constraints for the specified table.

        Args:
            table_name: Name of the target table

        Returns:
            List of foreign key definitions
        """
        return self.execute(f"PRAGMA foreign_key_list({table_name})")
    
    def show_table_foreign_key_info(self, table_name: str, foreign_key_name: str) -> List[str]:
        """Show table foreign key info"""
        return self.execute(f"PRAGMA foreign_key_info({table_name})")
    
    def show_table_views(self, table_name: str) -> List[str]:
        """Show table views"""
        return self.execute(f"PRAGMA view_list({table_name})")
    
    def show_table_view_info(self, table_name: str, view_name: str) -> List[str]:
        """Show table view info"""
        return self.execute(f"PRAGMA view_info({table_name})")
    
    def drop_table(self, table_name: str) -> None:
        """
        Drop the specified table if it exists.
        This operation cannot be undone.

        Args:
            table_name: Name of the table to drop

        Example:
            >>> db.drop_table("users")
        """
        return self.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    def drop_view(self, view_name: str) -> None:
        """
        Drop the specified view if it exists.
        This operation cannot be undone.

        Args:
            view_name: Name of the view to drop

        Example:
            >>> db.drop_view("active_users")
        """
        return self.execute(f"DROP VIEW IF EXISTS {view_name}")
    
    
    
    def __enter__(self):
        """
        Context manager entry point.
        Automatically connects to the database.

        Example:
            >>> with DatabaseManager("data.db") as db:
            ...     db.execute("SELECT * FROM users")
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point.
        Automatically disconnects from the database and handles cleanup.
        """
        self.disconnect() 