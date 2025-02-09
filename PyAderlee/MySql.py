"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

MySQL database management module for PyAderlee.
"""

import mysql.connector
from typing import List, Dict, Any, Union, Optional, Tuple
from pathlib import Path

class MySQLManager:
    """
    A class to handle MySQL database operations with built-in support for
    common database management tasks.

    Features:
    - CRUD operations (Create, Read, Update, Delete)
    - Table management (create, drop)
    - Schema inspection (tables, columns, indexes)
    - Foreign key and trigger management
    - Connection pooling support
    """
    def __init__(self, host: str, user: str, password: str, database: str, 
                 port: int = 3306, pool_size: int = 5):
        """
        Initialize MySQL manager with connection parameters.

        Args:
            host: MySQL server host
            user: MySQL username
            password: MySQL password
            database: Database name
            port: MySQL server port (default: 3306)
            pool_size: Connection pool size (default: 5)
        """
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database,
            'port': port,
            'pool_size': pool_size
        }
        self.connection = None
        self.cursor = None

    def connect(self) -> None:
        """
        Establish a connection to the MySQL database.
        Uses connection pooling for better performance.
        """
        try:
            self.connection = mysql.connector.connect(**self.config)
            self.cursor = self.connection.cursor(dictionary=True)
        except mysql.connector.Error as err:
            raise Exception(f"Failed to connect to MySQL: {err}")

    def disconnect(self) -> None:
        """
        Close the database connection and cleanup resources.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def execute(self, query: str, params: tuple = ()) -> Optional[List[Dict]]:
        """
        Execute an SQL query with optional parameters.

        Args:
            query: SQL query string
            params: Query parameters for parameterized queries

        Returns:
            List of dictionaries for SELECT queries, None for other queries

        Example:
            >>> db.execute("SELECT * FROM users WHERE age > %s", (25,))
            [{"id": 1, "name": "John", "age": 30}, {"id": 2, "name": "Jane", "age": 28}]
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()

        try:
            self.cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return None
        except mysql.connector.Error as err:
            self.connection.rollback()
            raise Exception(f"Query execution failed: {err}")

    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        Insert a single row of data into the specified table.

        Args:
            table_name: Name of the target table
            data: Dictionary mapping column names to their values

        Returns:
            Last inserted ID

        Example:
            >>> db.insert("users", {"name": "John", "age": 30})
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s' for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        self.execute(query, tuple(data.values()))
        return self.cursor.lastrowid

    def select(self, table_name: str, columns: List[str] = None, 
               where: Dict[str, Any] = None, limit: int = None) -> List[Dict]:
        """
        Select data from the specified table.

        Args:
            table_name: Name of the target table
            columns: List of column names to select (None for all)
            where: Dictionary of column-value pairs for WHERE clause
            limit: Maximum number of rows to return

        Returns:
            List of dictionaries containing the results

        Example:
            >>> db.select("users", ["name", "age"], {"age": 30}, limit=10)
        """
        cols = '*' if not columns else ', '.join(columns)
        query = f"SELECT {cols} FROM {table_name}"
        params = []

        if where:
            conditions = ' AND '.join([f"{k} = %s" for k in where.keys()])
            query += f" WHERE {conditions}"
            params.extend(where.values())

        if limit:
            query += f" LIMIT {limit}"

        return self.execute(query, tuple(params))

    def update(self, table_name: str, data: Dict[str, Any], 
               where: Dict[str, Any]) -> int:
        """
        Update existing records in the specified table.

        Args:
            table_name: Name of the target table
            data: Dictionary of column names and new values
            where: Dictionary of column-value pairs for WHERE clause

        Returns:
            Number of rows affected

        Example:
            >>> db.update("users", {"age": 31}, {"name": "John"})
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in where.keys()])
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        params = tuple(list(data.values()) + list(where.values()))
        
        self.execute(query, params)
        return self.cursor.rowcount

    def delete(self, table_name: str, where: Dict[str, Any]) -> int:
        """
        Delete records from the specified table.

        Args:
            table_name: Name of the target table
            where: Dictionary of column-value pairs for WHERE clause

        Returns:
            Number of rows affected

        Example:
            >>> db.delete("users", {"name": "John"})
        """
        conditions = ' AND '.join([f"{k} = %s" for k in where.keys()])
        query = f"DELETE FROM {table_name} WHERE {conditions}"
        
        self.execute(query, tuple(where.values()))
        return self.cursor.rowcount

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
