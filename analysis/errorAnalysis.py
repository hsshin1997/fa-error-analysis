# from collections import defaultdict
# from datetime import datetime, timedelta
# from typing import List, Tuple, Any

# def top_5_most_frequent_errors(entries: List) -> List[Tuple[str, int]]:
#     """Return the top 5 errors that occurred most frequently."""
#     occurrence_by_error_code = defaultdict(int)
    
#     for entry in entries:
#         occurrence_by_error_code[entry.err_code] += 1
    
#     top_5_errors = sorted(occurrence_by_error_code.items(), key=lambda x: x[1], reverse=True)[:5]
#     return top_5_errors

# def mean_time_between_failures(entries: List) -> float:
#     """Calculate Mean Time Between Failures (MTBF)."""
#     if len(entries) < 2:
#         return float('inf')  # If less than two entries, MTBF is undefined
    
#     # Sort entries by start time
#     sorted_entries = sorted(entries, key=lambda x: x.err_start)
    
#     total_time_between_failures = sum(
#         (sorted_entries[i].err_start - sorted_entries[i - 1].err_end).total_seconds()
#         for i in range(1, len(sorted_entries))
#     )
    
#     mtbf = total_time_between_failures / (len(sorted_entries) - 1)
#     return mtbf

# def mean_time_to_repair(entries: List) -> float:
#     """Calculate Mean Time To Repair (MTTR)."""
#     total_repair_time = sum(calculate_downtime(entry.err_start, entry.err_end) for entry in entries)
#     mttr = total_repair_time / len(entries) if entries else 0
#     return mttr

# def error_frequency_distribution(entries: List, time_interval: str = 'daily') -> dict:
#     """
#     Return error frequency distribution over a specified time interval.
    
#     Args:
#         entries: List of error DTOs.
#         time_interval: 'daily', 'weekly', or 'monthly'.
    
#     Returns:
#         A dictionary with time intervals as keys and occurrence counts as values.
#     """
#     frequency_distribution = defaultdict(int)
    
#     for entry in entries:
#         if time_interval == 'daily':
#             interval = entry.err_start.date()
#         elif time_interval == 'weekly':
#             interval = entry.err_start.strftime('%Y-%U')  # Year and week number
#         elif time_interval == 'monthly':
#             interval = entry.err_start.strftime('%Y-%m')  # Year and month
#         else:
#             raise ValueError("Invalid time_interval. Choose from 'daily', 'weekly', or 'monthly'.")
        
#         frequency_distribution[interval] += 1
    
#     return dict(frequency_distribution)

# def pareto_analysis(entries: List) -> List[Tuple[str, float]]:
#     """
#     Perform Pareto analysis (80/20 rule) on the errors by total downtime.
    
#     Returns:
#         A list of tuples with error codes and their cumulative percentage of downtime.
#     """
#     downtime_by_error_code = defaultdict(float)
    
#     for entry in entries:
#         downtime = calculate_downtime(entry.err_start, entry.err_end)
#         downtime_by_error_code[entry.err_code] += downtime
    
#     sorted_downtimes = sorted(downtime_by_error_code.items(), key=lambda x: x[1], reverse=True)
#     total_downtime = sum(downtime_by_error_code.values())
    
#     cumulative_percentage = 0.0
#     pareto_results = []
    
#     for err_code, downtime in sorted_downtimes:
#         cumulative_percentage += (downtime / total_downtime) * 100
#         pareto_results.append((err_code, cumulative_percentage))
#         if cumulative_percentage >= 80:
#             break
    
#     return pareto_results
