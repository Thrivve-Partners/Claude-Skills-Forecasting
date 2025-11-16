# Claude-Skills-Forecasting  
Forecasting Skills for Claude: Monte Carlo “When” & “How Many” for flow-based delivery  

## What this is  
This repository contains two skills for Claude that enable probabilistic forecasting in a flow-based delivery environment:  
- **MC When** — estimate *when* a given backlog will complete (given start date, throughput distribution, confidence level)  
- **MC How Many** — estimate *how many* items can be completed by a given date (using the same inputs)  

Both are designed to operate on throughput data (e.g., past completions from a Jira board or equivalent) and to support confidence-based planning rather than rigid commitments.

## Why it matters  
In a world where teams are working flow-based (rather than strictly sprint-based), it’s helpful to shift from “We will finish X items by Y date” to a more probabilistic mindset:  
- “Given our throughput history, we have a 70 % confidence to finish on or before date Z”  
- “We can reasonably expect to complete N items or more by date Z with 85 % confidence”  

These skills give product owners, managers and flow practitioners a lightweight way to bring Monte Carlo thinking into the conversation.

## What's included
- `thrivve-mc-when` — implementation of the *Monte Carlo When* skill
- `thrivve-mc-how-many` — implementation of the *Monte Carlo How Many* skill
- **Process Variation Checking** — automatic XMR control chart validation for data stability
- Other ancillary files (license, config templates, etc)

## Key Features

### Probabilistic Forecasting
Both skills use Monte Carlo simulation (10,000 iterations by default) to generate probability distributions rather than single-point estimates. This enables confidence-based planning: "We have an 85% chance of completing by date X" instead of rigid commitments.

### Automatic Process Variation Checking
The skills automatically validate your throughput data using **XMR (Individual and Moving Range) control charts** from Statistical Process Control. When you provide 20+ data points, the tools:

- Calculate natural process limits (UNPL, LNPL, URL)
- Identify outliers that may compromise forecast reliability
- Provide clear guidance on data quality and stability
- Help you distinguish between normal variation and process instability

**Why it matters**: Monte Carlo assumes your historical data represents future behavior. Outliers from one-time events (holidays, incidents, team changes) can distort forecasts. The variation check alerts you to investigate suspicious data points before making commitments.

**Example output**:
```
✓ PROCESS VARIATION CHECK
   Process stability confirmed.
   All throughput values are within natural process limits.
   Data is suitable for forecasting.
```

Or if outliers are detected:
```
⚠️ PROCESS VARIATION WARNING
   Variation check detected 2 individual outlier(s) and 1 range outlier(s).
   Forecast reliability may be affected by unstable process variation.

   Control Limits:
   - Upper Natural Process Limit (UNPL): 12.3 stories/day
   - Individual Outliers: [18, 22]

   Recommendation: Investigate outliers before relying on this forecast.
```

## How to get started  
1. Clone the repo:  
   ```bash  
   git clone https://github.com/Thrivve-Partners/Claude-Skills-Forecasting.git  
   cd Claude-Skills-Forecasting  
   
2. Add the Claude skills using **Settings → Capabilities → Upload Skill**
---

## Inputs

Both skills use **historical throughput** (count of completed items per day) to sample future outcomes.

- `throughput`: array of non-negative integers 
  e.g. `[5,3,1,3,4,6,5,3,1,3,2,5,0,0,2,0,1,0,2,4,3,4,0,1,0,0,2]`
- `confidence` (percentile): one of 50, 70, 85 (default 85), 95, 99
- Dates are ISO `YYYY-MM-DD` (timezone: your local system/Claude’s default unless given)

### MC How-Many (target date)
- `start_date`: when to begin forecasting (default: today)
- `target_date`: future date to stop
- Output: items forecast to complete by `target_date` at the chosen confidence

### MC When (backlog size)
- `start_date`: when to begin forecasting (default: today)
- `backlog_items`: positive integer
- Output: date by which `backlog_items` complete at the chosen confidence

---

## Example prompts (paste into Claude)

**How-Many:**
> If I have the following throughput `[5,3,1,3,4,6,5,3,1,3,2,5,0,0,2,0,1,0,2,4,3,4,0,1,0,0,2]`, can you tell me how many stories I will complete if I start today, and finish on the `2025-12-16`, with a certainty of `85%`?

**When:**
> We have `150` items to complete. Using throughput `[4,2,0,3,5,1,2,4,0,3,2,1,4,3]`, when will we finish at `85%` confidence if we start on `2025-11-03`?