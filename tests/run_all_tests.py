#!/usr/bin/env python3
"""
Main test runner for Monte Carlo Forecasting Skills.
Runs all test suites and reports overall results.
"""

import sys
import subprocess
from pathlib import Path

TESTS_DIR = Path(__file__).parent


def run_test_suite(test_script_name):
    """Run a test suite and return the result."""
    test_script = TESTS_DIR / test_script_name

    print(f"\n{'#'*70}")
    print(f"# Running: {test_script_name}")
    print(f"{'#'*70}\n")

    result = subprocess.run(
        ["python3", str(test_script)],
        capture_output=False,
        text=True
    )

    return result.returncode


def main():
    """Run all test suites."""
    print("="*70)
    print("MONTE CARLO FORECASTING SKILLS - FULL TEST SUITE")
    print("="*70)

    test_suites = [
        "test_mc_when.py",
        "test_mc_how_many.py"
    ]

    results = {}

    for suite in test_suites:
        returncode = run_test_suite(suite)
        results[suite] = returncode == 0

    # Overall summary
    print(f"\n{'='*70}")
    print("OVERALL TEST SUMMARY")
    print(f"{'='*70}")

    all_passed = True
    for suite, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{suite:30} {status}")
        if not passed:
            all_passed = False

    print(f"{'='*70}")

    if all_passed:
        print("\n🎉 All test suites passed!")
        return 0
    else:
        print("\n⚠️  Some test suites failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
