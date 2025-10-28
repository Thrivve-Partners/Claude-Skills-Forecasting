# Claude-Skills-Forecasting  
Forecasting Skills for Claude: Monte Carlo “When” & “How Many” for flow-based delivery.

## What this is  
This repository contains two Claude Skills that enable probabilistic forecasting in a flow-based delivery environment:  

**MC When** → Given:
- Start date (defaults to today if not specified)
- Number of items in the backlog (the number you want to complete)
- historical throughput data (i.e., historical completions per day)
- Confidence level (e.g., 85%)

It should return a range of possible completion dates — for example:
- “There’s an 85% chance that X items will be done **on or before** March 4th, 2026.”

**MC How Many** → Given:
- Start date (defaults to today if not specified)
- Target end date
- Historical throughput data
- Confidence level

It should return a range of how many items you can expect to finish by the target end date — for example:
- “There’s an 85% chance you’ll complete 42 **or more** items by March 18.”

## Why it matters  
As teams become more attentive to flow, it’s helpful to shift from a deterministic mindset — “We will finish X items by Y date” — to a probabilistic one, such as:
- “Given our historic throughput, we have a 70% confidence to finish on or before date Z.”
- “We can reasonably expect to complete N items or more by date Z with 85% confidence.”

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

## Inputs & Outputs

Both skills use historical throughput (count of completed items per day) to forecast future outcomes.
Inputs and outputs differ slightly depending on whether you want to forecast “how many” or “when.”

### Common inputs
- throughput: array of non-negative integers, oldest → newest, e.g. [5,3,1,3,4,6,5,3,1,3,2,5,0,0,2,0,1,0,2,4,3,4,0,1,0,0,2]
- confidence (percentile): one of 50, 70, 85, 95, 99 (default 85)
- start_date: ISO YYYY-MM-DD (optional - defaults to today if not specified; timezone: local/Claude’s default)

#### MC How-Many
- Additional input: target_date — future date to forecast up to
- Output: items forecast to complete by target_date at the chosen confidence

#### MC When
- Additional input: backlog_items — number of items to complete
- Output: date by which those items will complete at the chosen confidence

## Example prompts

### MC How-Many:

> If I have the following throughput [5,3,1,3,4,6,5,3,1,3,2,5,0,0,2,0,1,0,2,4,3,4,0,1,0,0,2],
> can you tell me how many stories I will complete if I start today and finish on 2025-12-16,
> with a certainty of 85%?

### MC When:

> We have 150 items to complete.
> Using throughput [4,2,0,3,5,1,2,4,0,3,2,1,4,3],
> when will we finish at 85% confidence if we start on 2025-11-03?
