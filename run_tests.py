#!/usr/bin/env python3
"""
Test runner script for enum_types tests
"""
import os
import subprocess
import sys


def run_tests():
    """Run the enum_types test suite"""
    
    # Change to the python directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Get the python executable path
    python_exe = "/Users/kris/Repos/pgnc-external-stack/.venv/bin/python"
    
    print("Running enum_types test suite...")
    print("=" * 50)
    
    # Run tests with coverage
    cmd = [
        python_exe, "-m", "pytest", 
        "tests/enum_types/", 
        "--cov=bin/data-load/db/enum_types",
        "--cov-report=term-missing",
        "--cov-report=html",
        "-v"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"\n💥 Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_tests())
