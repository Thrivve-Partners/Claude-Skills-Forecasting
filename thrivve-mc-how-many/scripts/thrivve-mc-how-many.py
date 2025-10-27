#!/usr/bin/env python3
"""
Monte Carlo simulation for forecasting story completion based on historical throughput.
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


def monte_carlo_how_many(
    throughput: List[int],
    target_date: str,
    confidence_level: float = 85.0,
    num_simulations: int = 10000,
    start_date: str = None
) -> dict:
    """
    Run Monte Carlo simulation to forecast story completion.
    
    Args:
        throughput: List of daily throughput values (stories completed per day)
        target_date: Future date to forecast for (string format)
        confidence_level: Desired confidence level as percentage (e.g., 85 for 85%)
        num_simulations: Number of Monte Carlo simulations to run
        start_date: Optional start date (defaults to today)
    
    Returns:
        Dictionary with simulation results including:
        - stories_at_confidence: Number of stories at the specified confidence level
        - percentiles: Dictionary of common percentiles (P10, P25, P50, P75, P85, P90, P95)
        - mean: Mean stories completed
        - min: Minimum stories in simulations
        - max: Maximum stories in simulations
        - days_until_target: Number of working days until target date
        - throughput_stats: Statistics about input throughput
    """
    
    if not throughput or len(throughput) < 10:
        raise ValueError("Throughput data must contain at least 10 days of data")
    
    if not 0 < confidence_level < 100:
        raise ValueError("Confidence level must be between 0 and 99 (100% confidence is not possible in probabilistic forecasting)")
    
    # Parse dates
    if start_date:
        start = parse_date(start_date)
    else:
        start = datetime.now()
    
    target = parse_date(target_date)
    
    if target <= start:
        raise ValueError("Target date must be in the future")
    
    # Calculate number of days
    days_until_target = (target - start).days
    
    # Run simulations
    simulation_results = []
    
    for _ in range(num_simulations):
        total_stories = 0
        for _ in range(days_until_target):
            # Randomly sample from historical throughput
            daily_throughput = random.choice(throughput)
            total_stories += daily_throughput
        simulation_results.append(total_stories)
    
    # Sort results for percentile calculations
    simulation_results.sort()
    
    # Calculate percentiles
    def get_percentile(data: List[int], percentile: float) -> int:
        """Get the value at a given percentile."""
        index = int((percentile / 100.0) * len(data))
        return data[min(index, len(data) - 1)]
    
    percentiles = {
        'P5': get_percentile(simulation_results, 95),
        'P25': get_percentile(simulation_results, 75),
        'P50': get_percentile(simulation_results, 50),
        'P70': get_percentile(simulation_results, 30),
        'P85': get_percentile(simulation_results, 15),
        'P95': get_percentile(simulation_results, 5),
        'P99': get_percentile(simulation_results, 1)
    }
    
    # Get value at specified confidence level
    # For "at least X with Y% confidence", we need the (100-Y) percentile
    # E.g., 85% confidence of "at least" = 15th percentile (P15)
    inverse_percentile = 100 - confidence_level
    stories_at_confidence = get_percentile(simulation_results, inverse_percentile)
    
    # Calculate throughput statistics
    throughput_mean = sum(throughput) / len(throughput)
    throughput_min = min(throughput)
    throughput_max = max(throughput)
    
    return {
        'stories_at_confidence': stories_at_confidence,
        'confidence_level': confidence_level,
        'percentiles': percentiles,
        'mean': sum(simulation_results) / len(simulation_results),
        'min': min(simulation_results),
        'max': max(simulation_results),
        'days_until_target': days_until_target,
        'target_date': target_date,
        'start_date': start.strftime('%Y-%m-%d'),
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
    output.append("MONTE CARLO 'HOW MANY' SIMULATION RESULTS")
    output.append("=" * 60)
    output.append("")
    
    output.append(f"📊 FORECAST SUMMARY")
    output.append(f"   Target Date: {results['target_date']}")
    output.append(f"   Start Date: {results['start_date']}")
    output.append(f"   Days Until Target: {results['days_until_target']} days")
    output.append(f"   Simulations Run: {results['num_simulations']:,}")
    output.append("")
    
    output.append(f"✨ ANSWER AT {results['confidence_level']}% CONFIDENCE")
    output.append(f"   You will complete {results['stories_at_confidence']} stories OR MORE")
    output.append(f"   by {results['target_date']} if you start on {results['start_date']}")
    output.append(f"   with {results['confidence_level']}% confidence")
    output.append(f"   (There's a {results['confidence_level']:.0f}% chance of completing {results['stories_at_confidence']} stories or more)")
    output.append("")
    
    output.append("📈 PERCENTILE FORECAST")
    # Always display these percentiles in order
    percentile_order = ['P99', 'P95', 'P85', 'P70', 'P50']
    for label in percentile_order:
        if label in results['percentiles']:
            output.append(f"   {label}: {results['percentiles'][label]} stories")
    output.append("")
    
    output.append("📉 STATISTICAL SUMMARY")
    output.append(f"   Mean (Average): {results['mean']:.1f} stories")
    output.append(f"   Range: {results['min']} - {results['max']} stories")
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
        print("Usage: monte_carlo_how_many.py <throughput> <target_date> [confidence_level] [num_simulations] <start_date>")
        print("\nExample:")
        print('  monte_carlo_how_many.py "3,5,4,2,6,4,5,3,7,4,5,6,3,4,5" "2025-12-31" 85 "2025-10-27"')
        print("\nArguments:")
        print("  throughput:        Comma-separated list of daily story counts (min 10 days)")
        print("  target_date:       Future date in YYYY-MM-DD or other common format")
        print("  confidence_level:  Confidence percentage (default: 85)")
        print("  num_simulations:   Number of simulations (default: 10000)")
        print("  start_date:        Start date in YYYY-MM-DD or other common format (default: none)")
        sys.exit(1)
    
    # Parse throughput
    throughput_str = sys.argv[1]
    throughput = [int(x.strip()) for x in throughput_str.split(',')]
    
    # Parse target date
    target_date = sys.argv[2]
    
    # Parse optional confidence level
    confidence_level = float(sys.argv[3]) if len(sys.argv) > 3 else 85.0
    
    # Parse optional number of simulations
    num_simulations = int(sys.argv[4]) if len(sys.argv) > 4 else 10000
    
    # Parse optional start date
    start_date = sys.argv[5] if len(sys.argv) > 5 else none   
    
    try:
        results = monte_carlo_how_many(
            throughput=throughput,
            target_date=target_date,
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
