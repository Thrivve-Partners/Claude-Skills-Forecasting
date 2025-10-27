# Monte Carlo Simulation Methodology

## Overview

Monte Carlo simulation is a statistical technique that uses random sampling to forecast outcomes based on historical data. For throughput forecasting, it answers "how many items will we complete by date X?"

## How It Works

1. **Historical Data**: Collect daily throughput values (e.g., stories completed per day)
2. **Random Sampling**: For each day until the target date, randomly select a throughput value from historical data
3. **Simulation**: Sum the randomly selected values to get total items completed
4. **Repetition**: Run thousands of simulations to build a probability distribution
5. **Analysis**: Calculate percentiles to determine confidence levels

## Example

Given throughput: [3, 5, 4, 2, 6, 4, 5, 3, 7, 4]
Target: 20 days from now

One simulation might randomly select:
- Day 1: 5, Day 2: 3, Day 3: 4, Day 4: 6, ... Day 20: 4
- Total: 87 stories

After 10,000 simulations, we might find:
- 50% of simulations: 80-90 stories
- 85% of simulations: ≤95 stories
- 95% of simulations: ≤100 stories

## Confidence Levels

The confidence level represents the probability that you will complete **at least** the forecasted number of stories.

Common confidence levels:
- **50% (P50)**: Median outcome - equal chance of completing more or fewer
- **85% (P15)**: Conservative - 85% chance of completing at least this many (only 15% chance of fewer)
- **95% (P5)**: Very conservative - 95% chance of completing at least this many (only 5% chance of fewer)
- **99% (P1)**: Maximum practical confidence - 99% chance of completing at least this many (only 1% chance of fewer)

**Important**: For "at least X with Y% confidence", the calculation uses the inverse percentile (100-Y). This means:
- 85% confidence → P15 (15th percentile)
- 90% confidence → P10 (10th percentile)
- 95% confidence → P5 (5th percentile)
- 99% confidence → P1 (1st percentile)

**Why 100% confidence is impossible**: In probabilistic forecasting, there's always uncertainty. Even with 10,000 simulations, there's always a small chance of an extreme outcome. 100% confidence would require absolute certainty, which doesn't exist in real-world forecasting. The practical maximum is 99%.

**Example**: If P15 = 275 stories, you have an 85% chance of completing at least 275 stories (and only a 15% chance of completing fewer).

## Assumptions

1. **Historical patterns continue**: Past throughput is representative of future performance
2. **Independence**: Each day's throughput is independent (not affected by previous days)
3. **Random sampling**: Any historical value can occur on any future day with equal probability

## Limitations

- Does not account for trends (improving/declining performance)
- Assumes team size and conditions remain constant
- Does not model dependencies between work items
- Weekends/holidays treated as regular days unless specified otherwise

## When to Use

Best for:
- Teams with stable throughput patterns
- Short to medium-term forecasts (weeks to months)
- Planning with uncertainty in mind

Not ideal for:
- New teams without history
- Major upcoming changes (team size, process, etc.)
- Very long-term forecasts (>6 months)
