#!/usr/bin/env python

"""
Run all standalone tests without requiring pytest or other dependencies.
This script can be used to validate basic functionality even if the full
environment is not set up.
"""

import importlib.util
import os
import sys


def is_standalone_test_file(filename):
    """Check if a file is a standalone test file."""
    return (filename.startswith('test_') and 
            filename.endswith('_standalone.py') and 
            filename != 'run_standalone_tests.py')


def import_module_from_file(module_name, file_path):
    """Import a module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def run_test_file(file_path):
    """Run a standalone test file and return success status."""
    module_name = os.path.basename(file_path).replace('.py', '')
    
    try:
        module = import_module_from_file(module_name, file_path)
        
        # If the module has a run_standalone_test function, call it
        if hasattr(module, 'run_standalone_test'):
            result = module.run_standalone_test()
            return result
        
        # Otherwise assume it ran successfully if it imported without error
        return True
    except Exception as e:
        print(f"Error running {file_path}: {e}")
        return False


def main():
    """Find and run all standalone test files."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    print("=== Running Standalone Tests ===")
    
    test_files = [f for f in os.listdir(current_dir) 
                 if is_standalone_test_file(f)]
    
    if not test_files:
        print("No standalone test files found.")
        return
    
    successes = 0
    failures = 0
    
    for test_file in sorted(test_files):
        file_path = os.path.join(current_dir, test_file)
        print(f"\nRunning {test_file}...")
        
        if run_test_file(file_path):
            print(f"✓ {test_file} PASSED")
            successes += 1
        else:
            print(f"✗ {test_file} FAILED")
            failures += 1
    
    print("\n=== Test Summary ===")
    print(f"Total tests: {len(test_files)}")
    print(f"Passed: {successes}")
    print(f"Failed: {failures}")
    
    return failures == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)