#!/usr/bin/env python3
"""
Monte Carlo simulation for forecasting completion date based on stories remaining and historical throughput.
"""

import sys
import random
from datetime import datetime, timedelta
from typing import List, Tuple
import json


def parse_date(date_str: str) -> datetime:
    """Parse a date string in various common formats."""
    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
        "%m-%d-%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y"
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse date: {date_str}")


def monte_carlo_when(
    throughput: List[int],
    stories_remaining: int,
    confidence_level: float = 85.0,
    num_simulations: int = 10000,
    start_date: str = None
) -> dict:
    """
    Run Monte Carlo simulation to forecast completion date.
    
    Args:
        throughput: List of daily throughput values (stories completed per day)
        stories_remaining: Number of stories that need to be completed
        confidence_level: Desired confidence level as percentage (e.g., 85 for 85%)
        num_simulations: Number of Monte Carlo simulations to run
        start_date: Optional start date (defaults to today)
    
    Returns:
        Dictionary with simulation results including:
        - completion_date_at_confidence: Date when work will be done at specified confidence
        - percentiles: Dictionary of common percentile dates (P25, P50, P70, P85, P95, P99)
        - days_percentiles: Dictionary of days required at each percentile
        - mean_date: Mean completion date
        - mean_days: Mean days to completion
        - min_date: Earliest completion in simulations
        - max_date: Latest completion in simulations
        - throughput_stats: Statistics about input throughput
    """
    
    if not throughput or len(throughput) < 10:
        raise ValueError("Throughput data must contain at least 10 days of data")
    
    if stories_remaining <= 0:
        raise ValueError("Stories remaining must be greater than 0")
    
    if not 0 < confidence_level < 100:
        raise ValueError("Confidence level must be between 0 and 99 (100% confidence is not possible in probabilistic forecasting)")
    
    # Parse start date
    if start_date:
        start = parse_date(start_date)
    else:
        start = datetime.now()
    
    # Run simulations
    simulation_days = []
    
    for _ in range(num_simulations):
        stories_completed = 0
        days = 0
        
        # Keep going until we've completed all stories
        while stories_completed < stories_remaining:
            # Randomly sample from historical throughput
            daily_throughput = random.choice(throughput)
            stories_completed += daily_throughput
            days += 1
        
        simulation_days.append(days)
    
    # Sort results for percentile calculations
    simulation_days.sort()
    
    # Calculate percentiles
    def get_percentile(data: List[int], percentile: float) -> int:
        """Get the value at a given percentile."""
        index = int((percentile / 100.0) * len(data))
        return data[min(index, len(data) - 1)]
    
    days_percentiles = {
        'P25': get_percentile(simulation_days, 25),
        'P50': get_percentile(simulation_days, 50),
        'P70': get_percentile(simulation_days, 70),
        'P85': get_percentile(simulation_days, 85),
        'P95': get_percentile(simulation_days, 95),
        'P99': get_percentile(simulation_days, 99)
    }
    
    # Get days at specified confidence level
    # For "done by X date with Y% confidence", we need the Y percentile
    # E.g., 85% confidence of "done by" = 85th percentile (P85)
    days_at_confidence = get_percentile(simulation_days, confidence_level)
    
    # Convert days to dates
    def days_to_date(days: int) -> datetime:
        return start + timedelta(days=days)
    
    completion_date_at_confidence = days_to_date(days_at_confidence)
    
    percentile_dates = {
        key: days_to_date(days).strftime('%Y-%m-%d')
        for key, days in days_percentiles.items()
    }
    
    mean_days = sum(simulation_days) / len(simulation_days)
    mean_date = days_to_date(int(mean_days))
    
    # Calculate throughput statistics
    throughput_mean = sum(throughput) / len(throughput)
    throughput_min = min(throughput)
    throughput_max = max(throughput)
    
    return {
        'completion_date_at_confidence': completion_date_at_confidence.strftime('%Y-%m-%d'),
        'days_at_confidence': days_at_confidence,
        'confidence_level': confidence_level,
        'percentile_dates': percentile_dates,
        'days_percentiles': days_percentiles,
        'mean_date': mean_date.strftime('%Y-%m-%d'),
        'mean_days': mean_days,
        'min_date': days_to_date(min(simulation_days)).strftime('%Y-%m-%d'),
        'min_days': min(simulation_days),
        'max_date': days_to_date(max(simulation_days)).strftime('%Y-%m-%d'),
        'max_days': max(simulation_days),
        'start_date': start.strftime('%Y-%m-%d'),
        'stories_remaining': stories_remaining,
        'num_simulations': num_simulations,
        'throughput_stats': {
            'samples': len(throughput),
            'mean': throughput_mean,
            'min': throughput_min,
            'max': throughput_max
        }
    }


def format_results(results: dict) -> str:
    """Format simulation results as human-readable text."""
    output = []
    output.append("=" * 60)
    output.append("MONTE CARLO 'WHEN' SIMULATION RESULTS")
    output.append("=" * 60)
    output.append("")
    
    output.append(f"📊 FORECAST SUMMARY")
    output.append(f"   Stories Remaining: {results['stories_remaining']}")
    output.append(f"   Start Date: {results['start_date']}")
    output.append(f"   Simulations Run: {results['num_simulations']:,}")
    output.append("")
    
    output.append(f"✨ ANSWER AT {results['confidence_level']}% CONFIDENCE")
    output.append(f"   You will complete the work on or before {results['completion_date_at_confidence']}")
    output.append(f"   ({results['days_at_confidence']} days from start date)")
    output.append(f"   with {results['confidence_level']}% confidence")
    output.append(f"   (There's a {results['confidence_level']:.0f}% chance of finishing on or before this date)")
    output.append("")
    
    output.append("📅 PERCENTILE FORECAST (Dates)")
    # Display percentiles from optimistic to conservative
    percentile_order = ['P25', 'P50', 'P70', 'P85', 'P95', 'P99']
    for label in percentile_order:
        if label in results['percentile_dates']:
            days = results['days_percentiles'][label]
            date = results['percentile_dates'][label]
            output.append(f"   {label}: {date} ({days} days)")
    output.append("")
    
    output.append("📈 STATISTICAL SUMMARY")
    output.append(f"   Mean (Average): {results['mean_date']} ({results['mean_days']:.1f} days)")
    output.append(f"   Best Case: {results['min_date']} ({results['min_days']} days)")
    output.append(f"   Worst Case: {results['max_date']} ({results['max_days']} days)")
    output.append("")
    
    output.append("📋 HISTORICAL THROUGHPUT")
    output.append(f"   Sample Size: {results['throughput_stats']['samples']} days")
    output.append(f"   Average Daily: {results['throughput_stats']['mean']:.1f} stories/day")
    output.append(f"   Range: {results['throughput_stats']['min']} - {results['throughput_stats']['max']} stories/day")
    output.append("")
    
    output.append("=" * 60)
    
    return "\n".join(output)


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3:
        print("Usage: thrivve-mc-when.py <throughput> <stories_remaining> [confidence_level] [num_simulations] [start_date]")
        print("\nExample:")
        print('  thrivve-mc-when.py "3,5,4,2,6,4,5,3,7,4,5,6,3,4,5" 100 85 10000 "2025-10-27"')
        print("\nArguments:")
        print("  throughput:         Comma-separated list of daily story counts (min 10 days)")
        print("  stories_remaining:  Number of stories to complete")
        print("  confidence_level:   Confidence percentage (default: 85)")
        print("  num_simulations:    Number of simulations (default: 10000)")
        print("  start_date:         Start date in YYYY-MM-DD or other common format (default: today)")
        sys.exit(1)
    
    # Parse throughput
    throughput_str = sys.argv[1]
    throughput = [int(x.strip()) for x in throughput_str.split(',')]
    
    # Parse stories remaining
    stories_remaining = int(sys.argv[2])
    
    # Parse optional confidence level
    confidence_level = float(sys.argv[3]) if len(sys.argv) > 3 else 85.0
    
    # Parse optional number of simulations
    num_simulations = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
    
    # Parse optional start date
    start_date = sys.argv[5] if len(sys.argv) > 5 else None
    
    try:
        results = monte_carlo_when(
            throughput=throughput,
            stories_remaining=stories_remaining,
            confidence_level=confidence_level,
            num_simulations=num_simulations,
            start_date=start_date
        )
        
        # Print formatted results
        print(format_results(results))
        
        # Also output JSON for programmatic access
        print("\nJSON Output:")
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
