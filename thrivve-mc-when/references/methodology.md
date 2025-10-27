# Monte Carlo 'When' Simulation Methodology

## Overview

Monte Carlo simulation is a statistical technique that uses random sampling to forecast outcomes based on historical data. For completion date forecasting, it answers "when will we complete X items?"

## How It Works

1. **Historical Data**: Collect daily throughput values (e.g., stories completed per day)
2. **Random Sampling**: For each simulated day, randomly select a throughput value from historical data
3. **Simulation**: Continue sampling days until the target number of stories is reached
4. **Repetition**: Run thousands of simulations to build a probability distribution of completion dates
5. **Analysis**: Calculate percentiles to determine confidence levels

## Example

Given throughput: [3, 5, 4, 2, 6, 4, 5, 3, 7, 4]
Stories remaining: 50

One simulation might randomly select:
- Day 1: 5 (total: 5)
- Day 2: 3 (total: 8)
- Day 3: 4 (total: 12)
- ...
- Day 11: 4 (total: 51) ✓ DONE
- Result: 11 days to complete

After 10,000 simulations, we might find:
- 50% of simulations: Complete within 11 days
- 85% of simulations: Complete within 13 days
- 95% of simulations: Complete within 15 days

## Confidence Levels

The confidence level represents the probability that you will complete the work **on or before** the forecasted date.

Common confidence levels:
- **25% (P25)**: Optimistic - Only 25% chance of finishing this early (75% chance it will take longer)
- **50% (P50)**: Median outcome - Equal chance of finishing earlier or later
- **70% (P70)**: Balanced - 70% chance of finishing by this date (30% chance of taking longer)
- **85% (P85)**: Conservative - 85% chance of finishing by this date (15% chance of taking longer)
- **95% (P95)**: Very conservative - 95% chance of finishing by this date (5% chance of taking longer)
- **99% (P99)**: Maximum practical confidence - 99% chance of finishing by this date (1% chance of taking longer)

**Important**: For "done on or before date X with Y% confidence", the calculation uses the Y percentile directly. This means:
- 85% confidence → P85 (85th percentile)
- 90% confidence → P90 (90th percentile)
- 95% confidence → P95 (95th percentile)
- 99% confidence → P99 (99th percentile)

**Why 100% confidence is impossible**: In probabilistic forecasting, there's always uncertainty. Even with 10,000 simulations, there's always a small chance of an extreme outcome. 100% confidence would require absolute certainty, which doesn't exist in real-world forecasting. The practical maximum is 99%.

**Example**: If P85 = December 15th (23 days), you have an 85% chance of completing all work by December 15th (and only a 15% chance it will take longer).

## Difference from 'How Many' Forecasting

### 'When' Forecasting (this skill):
- **Question**: "When will I finish N stories?"
- **Input**: Stories remaining, throughput history
- **Output**: Completion date
- **Percentile interpretation**: P85 means 85% chance of finishing BY this date
- **Higher confidence = Later date** (more buffer time)

### 'How Many' Forecasting:
- **Question**: "How many stories by date X?"
- **Input**: Target date, throughput history
- **Output**: Number of stories
- **Percentile interpretation**: P15 (at 85% confidence) means 85% chance of completing AT LEAST this many
- **Higher confidence = Fewer stories** (more conservative estimate)

## Assumptions

1. **Historical patterns continue**: Past throughput is representative of future performance
2. **Independence**: Each day's throughput is independent (not affected by previous days)
3. **Random sampling**: Any historical value can occur on any future day with equal probability
4. **Constant scope**: The number of stories remaining doesn't change during the forecast period

## Limitations

- Does not account for trends (improving/declining performance)
- Assumes team size and conditions remain constant
- Does not model dependencies between work items
- Weekends/holidays treated as regular days unless specified otherwise
- Does not account for scope changes or newly discovered work

## When to Use

Best for:
- Teams with stable throughput patterns
- Estimating delivery dates for backlogs
- Planning with uncertainty in mind
- Providing stakeholders with probabilistic commitments

Not ideal for:
- New teams without history
- Major upcoming changes (team size, process, etc.)
- Very large backlogs (>500 items)
- Projects with high variability in story complexity

## Practical Tips

1. **Use 85% confidence for commitments**: It provides a good balance between optimism and conservatism
2. **Show the range**: Share P50, P70, and P85 dates to illustrate uncertainty
3. **Update regularly**: Re-run forecasts as you complete work and gather more throughput data
4. **Consider the worst case**: The P95 or P99 date can help with risk planning
5. **Combine with charts**: Visual representations help communicate uncertainty
