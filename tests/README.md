# Monte Carlo Forecasting Skills - Test Suite

Automated tests for validating process variation checking and forecast generation in both Monte Carlo skills.

## Quick Start

Run all tests:
```bash
python3 tests/run_all_tests.py
```

Run individual test suites:
```bash
# Test MC When
python3 tests/test_mc_when.py

# Test MC How Many
python3 tests/test_mc_how_many.py
```

## Test Structure

```
tests/
├── run_all_tests.py          # Main test runner (runs all test suites)
├── test_mc_when.py           # Test suite for MC When skill
├── test_mc_how_many.py       # Test suite for MC How Many skill
├── test_data/
│   └── test_scenarios.json   # Test scenarios and expected results
└── expected_outputs/         # (Reserved for future use)
```

## Test Scenarios

All tests use the scenarios defined in `test_data/test_scenarios.json`:

### 1. Insufficient Data
- **Throughput**: 15 data points
- **Expected**: Variation check skipped (< 20 points required)
- **Status**: `insufficient_data`

### 2. Stable Process
- **Throughput**: 20 stable data points
- **Expected**: No outliers detected
- **Status**: `stable`
- **Outliers**: None

### 3. Process with Outliers
- **Throughput**: 20 points including outliers (18, 22)
- **Expected**: Outliers detected
- **Status**: `outliers_detected`
- **Individual Outliers**: 1 (value 22)
- **Moving Range Outliers**: 2 (ranges 20, 18)

### 4. Edge Case (Exactly 20 Points)
- **Throughput**: Exactly 20 data points
- **Expected**: Stable process (boundary test)
- **Status**: `stable`

### 5. High Variability
- **Throughput**: 20 points with high but stable variation
- **Expected**: No outliers (normal variability)
- **Status**: `stable`

## What Gets Tested

Each test validates:

1. **Variation Check Status**
   - Correct status returned (insufficient_data, stable, outliers_detected)
   - Data point count matches expectation

2. **Outlier Detection**
   - Individual outlier count correct
   - Moving range outlier count correct
   - Specific outlier values identified correctly

3. **XMR Metrics Calculation**
   - UNPL (Upper Natural Process Limit)
   - LNPL (Lower Natural Process Limit)
   - URL (Upper Range Limit)

4. **Simulation Execution**
   - Scripts run without errors
   - JSON output parseable
   - All expected fields present

## Modifying Tests

### Adding New Test Scenarios

Edit `test_data/test_scenarios.json` to add new scenarios:

```json
{
  "scenarios": {
    "your_new_scenario": {
      "description": "Description of what this tests",
      "throughput": "comma,separated,values",
      "expected_variation_status": "stable|outliers_detected|insufficient_data",
      "expected_data_points": 20,
      "expected_outliers": {
        "individual_count": 0,
        "range_count": 0
      }
    }
  }
}
```

### Changing Test Configuration

Modify forecast parameters in `test_scenarios.json`:

```json
{
  "when_tests": {
    "basic_forecast": {
      "stories_remaining": 50,
      "confidence_level": 85,
      "num_simulations": 1000,
      "start_date": "2025-11-16"
    }
  },
  "how_many_tests": {
    "basic_forecast": {
      "target_date": "2025-12-31",
      "confidence_level": 85,
      "num_simulations": 1000,
      "start_date": "2025-11-16"
    }
  }
}
```

**Note**: Tests use 1000 simulations (instead of 10,000) for faster execution while maintaining sufficient statistical validity.

## When to Run Tests

Run tests after:

- Modifying variation checking logic (`check_process_variation()`)
- Changing XMR control chart constants (2.66, 3.268)
- Updating output formatting in `format_results()`
- Making any changes to core simulation functions
- Before committing code changes
- After merging branches

## Test Output

### Successful Test
```
============================================================
Testing: stable_process
Description: 20+ data points with stable variation - no outliers
============================================================
✓ Variation status: stable
✓ Data points: 20
✓ Individual outlier count: 0
✓ Range outlier count: 0

Calculated Metrics:
   UNPL: 9.30
   LNPL: -0.50
   URL: 6.02

✅ PASSED: stable_process
```

### Failed Test
```
============================================================
Testing: process_with_outliers
Description: 20+ data points with outliers - should detect variation issues
============================================================
✓ Variation status: outliers_detected
✓ Data points: 20
❌ FAILED: Individual outlier count mismatch
   Expected: 1
   Actual: 0
```

## Test Coverage

Current test coverage includes:

- ✅ XMR control chart calculations (UNPL, LNPL, URL)
- ✅ Individual outlier detection
- ✅ Moving range outlier detection
- ✅ Insufficient data handling (< 20 points)
- ✅ Boundary conditions (exactly 20 points)
- ✅ High variability within normal limits
- ✅ JSON output formatting
- ✅ Both MC When and MC How Many skills

Not currently tested:

- ❌ Forecast accuracy (statistical distribution)
- ❌ Edge cases (negative throughput, invalid dates)
- ❌ Performance benchmarks
- ❌ Human-readable output formatting (only JSON validated)

## Continuous Integration

To integrate with CI/CD:

```bash
# Add to your CI pipeline
python3 tests/run_all_tests.py
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "Tests failed!"
    exit 1
fi
```

## Troubleshooting

### Tests fail with "Could not run simulation"
- Ensure Python scripts are executable: `chmod +x thrivve-mc-*/scripts/*.py`
- Verify Python 3 is installed: `python3 --version`

### JSON parsing errors
- Check that scripts haven't changed their output format
- Ensure "JSON Output:" marker is present in script output

### Unexpected test failures
- Run individual test suite with verbose output
- Check that `test_scenarios.json` matches current implementation
- Verify XMR constants (2.66, 3.268) haven't changed

## Contributing

When adding new features:

1. Add test scenarios to `test_scenarios.json`
2. Update expected outputs
3. Run tests to verify
4. Document new test cases in this README

## Future Enhancements

Planned test improvements:

- Performance benchmarking suite
- Edge case testing (invalid inputs, boundary conditions)
- Statistical accuracy validation
- Human-readable output validation
- Integration tests with sample Jira data
- Regression test suite with historical data
