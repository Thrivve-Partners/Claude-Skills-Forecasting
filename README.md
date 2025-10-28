# Claude-Skills-Forecasting  
Forecasting Skills for Claude: Monte Carlo “When” & “How Many” for flow-based delivery  

## What this is  
This repository contains two skills for Claude that enable probabilistic forecasting in a flow-based delivery environment:  
**MC When** → Given:
- Start date (defaults to today if not specified)
- Number of items in the backlog
- Throughput distribution (e.g., historical completions per day)
- Confidence level (e.g., 85%)
It should return a range of possible completion dates — for example:
- “There’s an 85% chance the backlog will be done on or before March 4.”

**MC How Many** → Given:
- Start date (defaults to today if not specified)
- Target end date
- Throughput distribution
- Confidence level
It should return a range of how many items you can expect to finish by that date — for example:
“There’s an 85% chance you’ll complete 42 or more items by March 18.”

## Why it matters  
In a world where teams are working flow-based (rather than strictly sprint-based), it’s helpful to shift from “We will finish X items by Y date” to a more probabilistic mindset:  
- “Given our throughput history, we have a 70 % confidence to finish on or before date Z”  
- “We can reasonably expect to complete N items or more by date Z with 85 % confidence”  

These skills give product owners, managers and flow practitioners a lightweight way to bring Monte Carlo thinking into the conversation.

## What’s included  
- `thrivve-mc-when` — implementation of the *Monte Carlo When* skill  
- `thrivve-mc-how-many` — implementation of the *Monte Carlo How Many* skill
- Other ancillary files (license, config templates, etc)  

## How to get started  
1. Clone the repo:  
   ```bash  
   git clone https://github.com/Thrivve-Partners/Claude-Skills-Forecasting.git  
   cd Claude-Skills-Forecasting  
   
2. Add the Claude skills using **Settings → Capabilities → Upload Skill**
---

## Inputs

Both skills use **historical throughput** (count of completed items per day) to sample future outcomes.

- `throughput`: array of non-negative integers, oldest → newest  
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