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

## Process Variation Checking (XMR Control Charts)

### Purpose

Before generating forecasts, the skill validates whether your historical throughput data exhibits **stable, predictable variation** suitable for Monte Carlo simulation. This is done using **XMR (Individual and Moving Range) control charts** from Statistical Process Control (SPC).

### Why It Matters

Monte Carlo simulation's core assumption is that **past data represents future behavior**. If your throughput contains outliers or shows unstable variation, this assumption breaks down:

- **Outliers** may represent one-time events (holiday, major incident, team reorganization) that won't recur
- **Unstable variation** signals a process in flux, making historical patterns unreliable for forecasting
- **Special cause variation** (outliers) must be distinguished from **common cause variation** (normal fluctuation)

As ProKanban research states: "If there are values outside of LNPL or UNPL lines, the system is objectively unstable therefore it shouldn't be used for forecasting."

### What Gets Checked (When You Have 20+ Data Points)

The XMR control chart calculates three key limits:

#### 1. UNPL (Upper Natural Process Limit)
```
UNPL = Average(Throughput) + (2.66 × Average(Moving Range))
```
Identifies **unusually high** throughput days (potential outliers above normal variation).

#### 2. LNPL (Lower Natural Process Limit)
```
LNPL = Average(Throughput) - (2.66 × Average(Moving Range))
```
Identifies **unusually low** throughput days (potential outliers below normal variation).

#### 3. URL (Upper Range Limit)
```
URL = 3.268 × Average(Moving Range)
```
Identifies **unstable day-to-day variation** (moving ranges that are abnormally large).

**Moving Range**: The absolute difference between consecutive throughput values
Example: For throughput [3, 7, 5], moving ranges are [|7-3|, |5-7|] = [4, 2]

### Statistical Constants Explained

- **2.66**: Represents 3 standard deviations for individual values (99.7% of stable data should fall within these limits)
- **3.268**: The D₄ constant from control chart theory for moving range upper limits

These represent **3-sigma limits** - approximately 99.7% of data from a stable process should fall within UNPL/LNPL bounds.

### Interpreting the Check Results

#### ✓ Process Stable (Green Light)
- All throughput values within UNPL/LNPL
- All moving ranges within URL
- **Meaning**: Your process exhibits only common cause variation (normal, predictable fluctuation)
- **Action**: Proceed with confidence - forecasts will be statistically reliable

#### ⚠️ Outliers Detected (Caution Required)
- One or more values exceed UNPL/LNPL OR moving ranges exceed URL
- **Meaning**: Your process exhibits special cause variation (unusual events or instability)
- **Impact on Forecast**:
  - May inflate variability, making forecasts unnecessarily pessimistic
  - May skew averages, distorting expected completion counts
  - Violates Monte Carlo's assumption of representative sampling

**What to Do**:
1. **Identify** which dates/values are outliers
2. **Investigate** the root cause:
   - Holiday with reduced capacity?
   - Major incident disrupting work?
   - Team size changed?
   - Process improvement implemented?
3. **Decide** whether to include or exclude:
   - **Exclude** if non-recurring (one-time event)
   - **Keep** if represents new normal (permanent change)
4. **Re-run** forecast with adjusted data

#### ℹ️ Insufficient Data (< 20 Points)
- Simulation runs, but variation check cannot be performed
- **Reason**: Need ~20 data points for control limits to be statistically reliable
- **Action**: Gather more data for validation, or proceed with awareness that stability is unverified

### Example

**Throughput**: [3, 5, 4, 2, 6, 4, 5, 3, 7, 4, 5, 6, 3, 4, 5, 2, 18, 4, 3, 5]
**Moving Ranges**: [2, 1, 2, 4, 2, 1, 2, 4, 3, 1, 1, 3, 1, 1, 3, 16, 14, 1, 2]

**Calculations**:
- Average Throughput: 4.85
- Average Moving Range: 3.63
- UNPL: 4.85 + (2.66 × 3.63) = **14.51**
- LNPL: 4.85 - (2.66 × 3.63) = **-4.81** (treat as 0 since throughput can't be negative)
- URL: 3.268 × 3.63 = **11.86**

**Result**: Value **18** exceeds UNPL (14.51) → **Outlier detected**
Moving ranges **16** and **14** exceed URL (11.86) → **Unstable variation detected**

**Recommendation**: Investigate day with 18 completions. Was this a sprint demo day with bulk story closures? One-time event? If so, consider excluding it and re-running the forecast.

### Why 20 Data Points?

From SPC research: "To ensure reliable estimates of sigma and the process average, one needs about 20 data points."

- **< 20 points**: Control limits change significantly with each new data point (unstable estimates)
- **20-30 points**: Control limits begin to stabilize (reliable estimates)
- **> 30 points**: Diminishing returns (limits don't change much)

The minimum of 10 points allows forecasting to run, but **variation checking requires 20+** for statistical validity.

### Integration with Monte Carlo Forecasting

1. **Automatic Check**: Runs every time before simulation (when 20+ points provided)
2. **Non-Blocking**: Forecast always generates (you decide whether to trust it)
3. **Transparent**: Shows exactly which values are outliers and the calculated limits
4. **Actionable**: Provides guidance on investigating and addressing outliers

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
