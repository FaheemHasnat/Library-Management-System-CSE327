#!/usr/bin/env python3
"""
Test runner script for Library Management System
Usage: python run_tests.py
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests using pytest."""
    try:
        # Change to project directory
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        
        # Run pytest
        cmd = [sys.executable, '-m', 'pytest', 'test/', '-v', '--tb=short']
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        print("PYTEST OUTPUT:")
        print("=" * 50)
        print(result.stdout)
        
        if result.stderr:
            print("\nERRORS:")
            print("=" * 50)
            print(result.stderr)
        
        print(f"\nTest execution completed with return code: {result.returncode}")
        return result.returncode
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
