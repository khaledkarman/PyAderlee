# PyAderlee

Version: 1.0

A lightweight Python library for data processing and file handling, inspired by pandas. This library provides simple and efficient tools for working with different file formats and data structures.

Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>

## Features

- File system operations with built-in format support
- JSON and CSV encoding/decoding
- Type-hinted methods for better IDE support
- Path handling using `pathlib`
- Flexible input types (str or Path objects)

## Installation

```bash
# First update pip
python.exe -m pip install --upgrade pip

# Local Installation
git clone https://github.com/rwasy/PyAderlee.git
cd PyAderlee
python setup.py install
# or
python -m pip install .
# or
pip install -e ./
# Coming soon to PyPI
pip install PyAderlee
```

## Quick Start

```python
from PyAderlee import FileSystem, Encoder

# Initialize filesystem with base path
fs = FileSystem("data/")

# Working with JSON
data = {"name": "John", "age": 30}
fs.write_json("person.json", data)
person = fs.read_json("person.json")

# Working with CSV
people = [
    {"name": "John", "age": 30},
    {"name": "Jane", "age": 25}
]
fs.write_csv("people.csv", people)
csv_data = fs.read_csv("people.csv")

# Direct encoding/decoding
encoder = Encoder()
json_str = encoder.to_json({"key": "value"})
csv_str = encoder.to_csv(people)
```

## API Reference

### FileSystem Class

#### Constructor
- `FileSystem(base_path: Union[str, Path] = None)`
  - Initialize with optional base path for all operations

#### Methods
- `read_file(filepath, encoding='utf-8')`: Read raw file contents
- `write_file(filepath, content, encoding='utf-8')`: Write content to file
- `read_json(filepath)`: Read and parse JSON file
- `write_json(filepath, data)`: Write data as JSON
- `read_csv(filepath, delimiter=',')`: Read CSV to list of dictionaries
- `write_csv(filepath, data, delimiter=',')`: Write list of dictionaries as CSV
- `list_files(pattern="*")`: List files matching pattern
- `exists(filepath)`: Check if file exists

### Encoder Class

#### Static Methods
- `to_json(data, indent=4)`: Convert data to JSON string
- `from_json(json_str)`: Parse JSON string to Python object
- `to_csv(data, delimiter=',')`: Convert list of dictionaries to CSV string

### DatabaseManager Class

#### Constructor
- `DatabaseManager(db_path: Union[str, Path])`
  - Initialize with SQLite database file path

#### Methods
- `connect()`: Establish database connection
- `disconnect()`: Close database connection
- `execute(query, params=())`: Execute raw SQL query
- `create_table(table_name, columns)`: Create new table
- `insert(table_name, data)`: Insert data into table
- `select(table_name, columns=None, where=None)`: Select data from table
- `update(table_name, data, where)`: Update data in table
- `delete(table_name, where)`: Delete data from table

Example usage:
```python
from PyAderlee import DatabaseManager

# Using context manager
with DatabaseManager("data.db") as db:
    # Create table
    db.create_table("users", {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "age": "INTEGER"
    })
    
    # Insert data
    db.insert("users", {"name": "John", "age": 30})
    
    # Query data
    results = db.select("users", where={"name": "John"})
```

## Testing

The library comes with a comprehensive test suite. To run the tests:

```bash
# Run all tests
python -m tests.run_tests

# Run specific test files
python -m unittest tests.test_encoder
python -m unittest tests.test_filesystem
```

### Test Coverage
- Encoder tests: JSON encoding/decoding, CSV conversion
- FileSystem tests: File operations, JSON/CSV handling, file listing
- Clean test environment with automatic setup/teardown

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Run the tests to ensure they pass
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
