"""
PyAderlee - Python Data Processing Library
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

A lightweight Python library for data processing and file handling.
"""

import os
from typing import Union, List, Dict, Any
from pathlib import Path
from .encoder import Encoder
import subprocess
class FileSystem:
    """
    A class to handle file system operations with built-in support for
    different file formats
    """
    def __init__(self, base_path: Union[str, Path] = None):
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.encoder = Encoder()
    
    def read_file(self, filepath: Union[str, Path], encoding: str = 'utf-8') -> str:
        """Read contents of a file"""
        full_path = self.base_path / Path(filepath)
        with open(full_path, 'r', encoding=encoding) as f:
            return f.read()
    
    def write_file(self, filepath: Union[str, Path], content: str, 
                   encoding: str = 'utf-8') -> None:
        """Write content to a file"""
        full_path = self.base_path / Path(filepath)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(full_path, 'w', encoding=encoding) as f:
            f.write(content)
    
    def read_json(self, filepath: Union[str, Path]) -> Any:
        """Read and parse JSON file"""
        content = self.read_file(filepath)
        return self.encoder.from_json(content)
    
    def write_json(self, filepath: Union[str, Path], data: Any) -> None:
        """Write data to JSON file"""
        content = self.encoder.to_json(data)
        self.write_file(filepath, content)
    
    def read_csv(self, filepath: Union[str, Path], delimiter: str = ',') -> List[Dict]:
        """Read CSV file and return list of dictionaries"""
        content = self.read_file(filepath)
        lines = content.strip().split('\n')
        
        if not lines:
            return []
        
        headers = lines[0].split(delimiter)
        result = []
        
        for line in lines[1:]:
            values = line.split(delimiter)
            row_dict = {headers[i]: values[i] for i in range(len(headers))}
            result.append(row_dict)
            
        return result
    
    def write_csv(self, filepath: Union[str, Path], data: List[Dict], 
                  delimiter: str = ',') -> None:
        """Write list of dictionaries to CSV file"""
        content = self.encoder.to_csv(data, delimiter)
        self.write_file(filepath, content)
    
    def list_files(self, pattern: str = "*") -> List[Path]:
        """List all files matching the pattern in base_path"""
        return list(self.base_path.glob(pattern))
    
    def exists(self, filepath: Union[str, Path]) -> bool:
        """Check if file exists"""
        return (self.base_path / Path(filepath)).exists()
    
    def exec(self, command: str) -> str:
        """Execute a command and return the output"""
        try:
            result = subprocess.getoutput(command)
        except Exception as e:
            result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8', errors='ignore')
            result = result.stdout
        return result.strip()
