"""
PyAderlee Test Runner
Version: 1.0
Copyright (c) 2025 Rawasy
Developer: Khaled Karman <k@rawasy.com>
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to Python path for importing PyAderlee
sys.path.insert(0, str(Path(__file__).parent.parent))

def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    start_dir = Path(__file__).parent
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1) 