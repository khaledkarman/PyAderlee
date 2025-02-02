"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

A lightweight Python library for data processing and file handling.
"""

from typing import List, Dict, Any
import json

class Encoder:
    """
    A class to handle encoding and decoding of various data formats

    
    """
    @staticmethod
    def to_json(data: Any, indent: int = 4) -> str:
        """Convert data to JSON string"""
        return json.dumps(data, indent=indent)
    
    @staticmethod
    def from_json(json_str: str) -> Any:
        """Parse JSON string to Python object"""
        return json.loads(json_str)
    
    @staticmethod
    def to_csv(data: List[Dict], delimiter: str = ',') -> str:
        """Convert list of dictionaries to CSV string"""
        if not data:
            return ""
        
        headers = list(data[0].keys())
        rows = [delimiter.join(headers)]
        
        for item in data:
            row = [str(item.get(header, '')) for header in headers]
            rows.append(delimiter.join(row))
            
        return '\n'.join(rows) 