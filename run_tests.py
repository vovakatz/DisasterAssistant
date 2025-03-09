#!/usr/bin/env python
"""
Test runner script for DisasterAssistant

This script provides a convenient way to run tests with proper
dependency handling.
"""

import argparse
import os
import sys
import subprocess


def run_standalone_tests():
    """Run the standalone tests that don't require dependencies."""
    print("\n== Running standalone tests ==\n")
    result = subprocess.run(
        [sys.executable, "tests/run_standalone_tests.py"],
        check=False
    )
    return result.returncode == 0


def run_pytest_utils():
    """Run the utils tests with pytest."""
    print("\n== Running pytest utils tests ==\n")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_utils.py", "-v"],
        check=False
    )
    return result.returncode == 0


def run_pytest_scrape():
    """Run the scrape service tests with pytest."""
    print("\n== Running pytest scrape service tests ==\n")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_scrape_service.py", "-v"],
        check=False
    )
    return result.returncode == 0


def run_all_working_tests():
    """Run all the tests that are known to work."""
    success = True
    
    if not run_standalone_tests():
        success = False
        print("\n❌ Standalone tests failed")
    else:
        print("\n✅ Standalone tests passed")
    
    if not run_pytest_utils():
        success = False
        print("\n❌ Pytest utils tests failed")
    else:
        print("\n✅ Pytest utils tests passed")
    
    # Skip scrape service test as it requires pytest-asyncio and OpenAI API access
    print("\n⚠️ Skipping scrape service tests (requires pytest-asyncio)")
    
    return success


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run DisasterAssistant tests")
    parser.add_argument(
        "--standalone", 
        action="store_true", 
        help="Run only standalone tests that don't require dependencies"
    )
    parser.add_argument(
        "--utils", 
        action="store_true", 
        help="Run only utils tests using pytest"
    )
    parser.add_argument(
        "--scrape", 
        action="store_true", 
        help="Run only scrape service tests using pytest"
    )
    
    args = parser.parse_args()
    
    # If no specific tests are requested, run all working tests
    if not (args.standalone or args.utils or args.scrape):
        success = run_all_working_tests()
    else:
        success = True
        if args.standalone and not run_standalone_tests():
            success = False
        if args.utils and not run_pytest_utils():
            success = False
        if args.scrape and not run_pytest_scrape():
            success = False
    
    print("\n== Test Summary ==")
    if success:
        print("✅ All selected tests passed")
        sys.exit(0)
    else:
        print("❌ Some tests failed")
        sys.exit(1)