---
name: thrivve-mc-how-many
description: Thrivve Partners Monte Carlo simulation to forecast story/task completion based on historical throughput. Use when the user asks "how many stories/tasks will be completed by [date]" with historical daily throughput data. Requires at least 10 days of throughput history and a future target date. Provides probabilistic forecasts at specified confidence levels (default 85%).
---

# Thrivve Partners Monte Carlo 'How Many' Forecasting

Forecast how many stories or tasks will be completed by a future date using Monte Carlo simulation based on historical throughput data.

## When to Use

Use this skill when the user provides:
1. Historical throughput data (daily counts for at least 10 days)
2. A future target date
3. A desired confidence level (optional, defaults to 85%)
4. A start date (optional, defaults to today)

Common trigger patterns:
- "In the last X days, the throughput has been [counts] - how many stories will I have completed by [date] with [confidence]% confidence?"
- "Based on throughput of [counts], how many will we finish by [date] if we start [date / 'today']?"
- "Run Monte Carlo simulation for [counts] over [X] days until [date]"

## Quick Start

Execute the Monte Carlo simulation script:

```bash
python scripts/thrivve-mc-how-many.py "<comma-separated-throughput>" "<target-date>" <confidence-level> "<start-date>"
```

Example:
```bash
python scripts/thrivve-mc-how-many.py "3,5,4,2,6,4,5,3,7,4,5,6,3,4,5" "2025-12-31" 85 "2025-10-27"
```

## Input Requirements

1. **Throughput data**: Minimum 10 days of daily completion counts
   - Format: Comma-separated integers (e.g., "3,5,4,2,6,4,5,3,7,4")
   - More data = better predictions (15-30 days recommended)

2. **Target date**: Future date in any common format
   - Supported formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, "Month DD, YYYY", etc.
   - Must be in the future

3. **Confidence level**: Percentage between 0-99 (default: 85)
   - 25%: Optimistic outcome (lower certainty, higher forecast)
   - 50%: Median outcome (equal chance of more or less)
   - 70%: Median outcome (equal chance of more or less)
   - 85%: Conservative (commonly used in agile forecasting)
   - 95%: Very conservative (high certainty, lower forecast)
   - 99%: Maximum practical confidence (extremely conservative)
   - Note: 100% confidence is not possible in probabilistic forecasting
   
4. **Start date**: A date in any common format (default: today)
   - Supported formats: YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY, "Month DD, YYYY", etc. 

## Output Format

The script provides:
- **Primary answer**: Stories at specified confidence level, for the future date given
- **Percentile forecasts**: P25, P50, P70, P85, P95, P99
- **Statistical summary**: Mean, min, max across all simulations
- **Throughput analysis**: Statistics about historical data
- **JSON output**: Structured data for further processing

## Workflow

1. Parse user's throughput data from their message
2. Extract target date and confidence level
3. Run the Monte Carlo script with parsed parameters
4. Present results in clear, actionable format
5. Explain what the confidence level means in context

## Interpreting Results

- **At X% confidence**: "There's an X% chance you'll complete AT LEAST this many stories" (uses the inverse percentile: 100-X)
- **P50 (median)**: Half of simulations had more, half had fewer
- **P15 (85% confidence)**: 85% of simulations completed more than this number
- **P85**: Only 15% of simulations exceeded this number (inverse: 15% confidence of "at least")
- **Range**: Shows best and worst cases from all simulations

**Example**: At 85% confidence, you'll complete AT LEAST 275 stories (P15), meaning there's only a 15% chance of completing fewer.

## Advanced Usage

Optional parameters:
- `num_simulations`: Number of Monte Carlo runs (default: 10,000)
  - Higher values increase accuracy but take longer
  - 10,000 is typically sufficient for reliable results

## Methodology

For detailed explanation of Monte Carlo simulation methodology, assumptions, and limitations, see `references/methodology.md`.

Key points:
- Uses random sampling from historical throughput
- Runs thousands of simulations to build probability distribution
- Assumes past patterns continue into the future
- Does not account for trends or changing conditions

## Example Interaction

User: "In the last 15 days, the throughput has been 3,5,4,2,6,4,5,3,7,4,5,6,3,4,5 - how many stories will I have completed by December 31st with 85% confidence, if I start today?"

Response steps:
1. Parse throughput: [3,5,4,2,6,4,5,3,7,4,5,6,3,4,5]
2. Parse target date: 2025-12-31
3. Parse confidence: 85%
4. Parse start date: today
5. Run simulation
6. Present results: "Given your start date of today, and a confidence of 85%, you will complete 275 stories OR MORE by December 31st, 2025 (there's only a 15% chance of completing fewer)"
7. Provide percentile context and explain the forecast
