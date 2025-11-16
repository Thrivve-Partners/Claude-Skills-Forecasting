#!/usr/bin/env python3
"""
Test suite for Monte Carlo 'How Many' simulation.
Tests variation checking and forecast generation.
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# Add parent directory to path to import the main script
TESTS_DIR = Path(__file__).parent
PROJECT_ROOT = TESTS_DIR.parent
MC_HOW_MANY_SCRIPT = PROJECT_ROOT / "thrivve-mc-how-many" / "scripts" / "thrivve-mc-how-many.py"


def load_test_scenarios():
    """Load test scenarios from JSON file."""
    scenarios_file = TESTS_DIR / "test_data" / "test_scenarios.json"
    with open(scenarios_file, 'r') as f:
        return json.load(f)


def run_mc_how_many(throughput, target_date, confidence_level, num_simulations, start_date):
    """Run the MC How Many script and return parsed JSON results."""
    cmd = [
        "python3",
        str(MC_HOW_MANY_SCRIPT),
        throughput,
        target_date,
        str(confidence_level),
        str(num_simulations),
        start_date
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error running MC How Many: {result.stderr}")
        return None

    # Parse JSON from output (it's after "JSON Output:" line)
    output_lines = result.stdout.split('\n')
    json_start = False
    json_lines = []

    for line in output_lines:
        if "JSON Output:" in line:
            json_start = True
            continue
        if json_start:
            json_lines.append(line)

    json_str = '\n'.join(json_lines)
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON output")
        return None


def test_variation_check(scenario_name, scenario_data, test_config):
    """Test variation checking for a given scenario."""
    print(f"\n{'='*60}")
    print(f"Testing: {scenario_name}")
    print(f"Description: {scenario_data['description']}")
    print(f"{'='*60}")

    result = run_mc_how_many(
        scenario_data['throughput'],
        test_config['target_date'],
        test_config['confidence_level'],
        test_config['num_simulations'],
        test_config['start_date']
    )

    if not result:
        print("❌ FAILED: Could not run simulation")
        return False

    variation = result.get('variation_check', {})

    # Check variation status
    expected_status = scenario_data['expected_variation_status']
    actual_status = variation.get('status')

    if actual_status != expected_status:
        print(f"❌ FAILED: Variation status mismatch")
        print(f"   Expected: {expected_status}")
        print(f"   Actual: {actual_status}")
        return False

    print(f"✓ Variation status: {actual_status}")

    # Check data points
    expected_points = scenario_data['expected_data_points']
    actual_points = variation.get('data_points')

    if actual_points != expected_points:
        print(f"❌ FAILED: Data points mismatch")
        print(f"   Expected: {expected_points}")
        print(f"   Actual: {actual_points}")
        return False

    print(f"✓ Data points: {actual_points}")

    # Check outliers if expected
    if 'expected_outliers' in scenario_data and actual_status != 'insufficient_data':
        expected_outliers = scenario_data['expected_outliers']
        actual_outliers = variation.get('outliers', {})

        # Check individual outlier count
        if 'individual_count' in expected_outliers:
            expected_count = expected_outliers['individual_count']
            actual_count = actual_outliers.get('individual_count', 0)

            if actual_count != expected_count:
                print(f"❌ FAILED: Individual outlier count mismatch")
                print(f"   Expected: {expected_count}")
                print(f"   Actual: {actual_count}")
                return False

            print(f"✓ Individual outlier count: {actual_count}")

        # Check range outlier count
        if 'range_count' in expected_outliers:
            expected_count = expected_outliers['range_count']
            actual_count = actual_outliers.get('range_count', 0)

            if actual_count != expected_count:
                print(f"❌ FAILED: Range outlier count mismatch")
                print(f"   Expected: {expected_count}")
                print(f"   Actual: {actual_count}")
                return False

            print(f"✓ Range outlier count: {actual_count}")

        # Check specific outlier values
        if 'individual_values_contains' in expected_outliers:
            expected_values = expected_outliers['individual_values_contains']
            actual_values = actual_outliers.get('individual_values', [])

            for expected_value in expected_values:
                if expected_value not in actual_values:
                    print(f"❌ FAILED: Expected outlier value {expected_value} not found")
                    print(f"   Actual values: {actual_values}")
                    return False

            print(f"✓ Individual outliers contain: {expected_values}")

        # Check specific moving range outliers
        if 'moving_ranges_contains' in expected_outliers:
            expected_ranges = expected_outliers['moving_ranges_contains']
            actual_ranges = actual_outliers.get('moving_ranges', [])

            for expected_range in expected_ranges:
                if expected_range not in actual_ranges:
                    print(f"❌ FAILED: Expected moving range outlier {expected_range} not found")
                    print(f"   Actual ranges: {actual_ranges}")
                    return False

            print(f"✓ Moving range outliers contain: {expected_ranges}")

    # Display metrics if available
    if 'metrics' in variation:
        metrics = variation['metrics']
        print(f"\nCalculated Metrics:")
        print(f"   UNPL: {metrics.get('unpl', 'N/A'):.2f}")
        print(f"   LNPL: {metrics.get('lnpl', 'N/A'):.2f}")
        print(f"   URL: {metrics.get('url', 'N/A'):.2f}")

    print(f"\n✅ PASSED: {scenario_name}")
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("MONTE CARLO 'HOW MANY' TEST SUITE")
    print("=" * 60)

    # Load test scenarios
    test_data = load_test_scenarios()
    scenarios = test_data['scenarios']
    test_config = test_data['how_many_tests']['basic_forecast']

    # Run tests
    passed = 0
    failed = 0

    for scenario_name, scenario_data in scenarios.items():
        try:
            if test_variation_check(scenario_name, scenario_data, test_config):
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ FAILED: {scenario_name} - {str(e)}")
            failed += 1

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Total tests: {passed + failed}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")

    if failed == 0:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
