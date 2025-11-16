# Claude-Skills-Forecasting  
Forecasting Skills for Claude: Monte Carlo “When” & “How Many” for flow-based delivery  

## What this is  
This repository contains two skills for Claude that enable probabilistic forecasting in a flow-based delivery environment:  
- **MC When** — forecast *when* a given backlog will complete (given start date, throughput distribution, confidence level)  
- **MC How Many** — forecast *how many* items can be completed by a given date (using the same inputs)  

Both are designed to operate on throughput data (e.g., past completions from a Jira board or equivalent) and to support confidence-based planning rather than rigid commitments.

## Why it matters  
In a world where teams are working in a flow-based manner rather than time-boxed iterations, it’s helpful to shift from “We will finish X items by Y date” to a more probabilistic mindset:  
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

- Calculate natural process limits (UNPL, URL)
- Identify outliers that may compromise forecast reliability
- Provide clear guidance on data quality and stability
- Help you distinguish between normal variation and process instability

**Why it matters**: Monte Carlo assumes your historical data represents future behavior. Outliers from one-time events (holidays, incidents, team changes), administrative activities (backlog cleanup, board hygiene), or batched work completion can distort forecasts. The variation check alerts you to investigate suspicious data points before you share your forecasted position.

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
### 1. Clone the Repository
```bash
git clone https://github.com/Thrivve-Partners/Claude-Skills-Forecasting.git  
cd Claude-Skills-Forecasting  
```

### 2. Create Zip Files for Each Skill

You need to zip each skill folder individually before uploading to Claude Desktop.

**Option A: Using the command line**
```bash
# For macOS/Linux
zip -r thrivve-mc-how-many.zip thrivve-mc-how-many
zip -r thrivve-mc-when.zip thrivve-mc-when

# For Windows (PowerShell)
Compress-Archive -Path thrivve-mc-how-many -DestinationPath thrivve-mc-how-many.zip
Compress-Archive -Path thrivve-mc-when -DestinationPath thrivve-mc-when.zip
```

**Option B: Manual zipping**
- Right-click on the `thrivve-mc-how-many` folder and select "Compress" (macOS) or "Send to → Compressed folder" (Windows)
- Repeat for the `thrivve-mc-when` folder

### 3. Upload Skills to Claude Desktop

1. Open **Claude Desktop** application
2. Click **Claude** in the menu bar (top-left on macOS)
3. Select **Settings...** (or press ⌘,)
4. In the left sidebar, click **Capabilities**
5. Click the **Upload skill** button (top-right)
6. Select the `thrivve-mc-how-many.zip` file
7. Repeat steps 5-6 for `thrivve-mc-when.zip`

Your skills should now appear in the Skills section and be ready to use!

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
> We have `150` items to complete. Using throughput `[5,3,1,3,4,6,5,3,1,3,2,5,0,0,2,0,1,0,2,4,3,4,0,1,0,0,2]`, when will we finish at `85%` confidence if we start on `2025-11-03`?