"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

A lightweight Python library for data processing and file handling.
"""

from .filesystem import FileSystem
from .encoder import Encoder
from .database import DatabaseManager
from .github import GitHub
from .MySql import MySQLManager
from .secure_data import SecureData
from .load_env import Environment

__version__ = "1.0"
__all__ = ['FileSystem', 'Encoder', 'DatabaseManager', 'GitHub', 'MySQLManager', 'SecureData', 'Environment'] 