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
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
    
    def disconnect(self) -> None:
        """Close database connection"""
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
        Insert data into table
        
        Args:
            table_name: Target table name
            data: Dictionary of column names and values
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute(query, tuple(data.values()))
    
    def select(self, table_name: str, columns: List[str] = None, 
               where: Dict[str, Any] = None) -> List[tuple]:
        """
        Select data from table
        
        Args:
            table_name: Target table name
            columns: List of columns to select (None for all)
            where: Dictionary of column-value pairs for WHERE clause
            
        Returns:
            List of query results
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
        Update data in table
        
        Args:
            table_name: Target table name
            data: Dictionary of column names and new values
            where: Dictionary of column-value pairs for WHERE clause
        """
        set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(where.values()))
        
        self.execute(query, params)
    
    def delete(self, table_name: str, where: Dict[str, Any]) -> None:
        """
        Delete data from table
        
        Args:
            table_name: Target table name
            where: Dictionary of column-value pairs for WHERE clause
        """
        conditions = ' AND '.join([f"{k} = ?" for k in where.keys()])
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        
        self.execute(query, tuple(where.values()))
    
    def create_table(self, table_name: str, columns: Dict[str, str]) -> None:
        """
        Create new table
        
        Args:
            table_name: Name of the table
            columns: Dictionary of column names and their SQL types
        """
        cols = [f"{name} {dtype}" for name, dtype in columns.items()]
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(cols)}) STRICT"
        self.execute(query)
    
    def show_tables(self) -> List[str]:
        """Show all tables in database"""
        return self.execute("SELECT name FROM sqlite_master WHERE type='table'")
    
    def show_columns(self, table_name: str) -> List[str]:
        """
        Show all columns in a table with their definitions.
        Returns the complete SQL schema information for the table.

        Args:
            table_name: Name of the table to inspect

        Returns:
            List of tuples containing schema information

        Example:
            >>> db.create_table("users", {
            ...     "id": "INTEGER PRIMARY KEY",
            ...     "name": "TEXT",
            ...     "age": "INTEGER"
            ... })
            >>> db.show_columns("users")
            [('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, age INTEGER) STRICT',)]

        Note:
            This method returns the raw SQL schema definition.
            For a more structured view of columns, use show_table_structure().
        """
        ret = self.execute(f"SELECT sql FROM sqlite_schema WHERE name='{table_name}'")
        return ret[0][0]
    
    def show_table_schema(self, table_name: str) -> List[str]:
        """Show table schema"""
        # return self.execute(f"PRAGMA table_info({table_name})")
        ret = self.execute(f"SELECT sql FROM sqlite_schema WHERE name='{table_name}'")
        return ret[0][0]
    

    def show_table_structure(self, table_name: str) -> List[str]:
        """Show table structure"""
        return self.execute(f"PRAGMA table_info({table_name})")
    
    def show_table_indexes(self, table_name: str) -> List[str]:
        """Show table indexes"""
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
        """Show table foreign keys"""
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
        """Drop table"""
        return self.execute(f"DROP TABLE IF EXISTS {table_name}")
    
    def drop_view(self, view_name: str) -> None:
        """Drop view"""
        return self.execute(f"DROP VIEW IF EXISTS {view_name}")
    
    
    
    def __enter__(self):
        """Context manager entry"""


        self.connect()


        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect() 