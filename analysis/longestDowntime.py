from datetime import datetime
from collections import defaultdict
from typing import Any, List, Tuple, Dict



def calculate_weekly_downtime(entries: List) -> Dict[int, List[Tuple[str, float]]]:
    """
    Calculate the top 5 longest total downtime for each week of the year.

    Args:
        entries: A list of StackerCraneErrorEntry objects.

    Returns:
        A dictionary where keys are week numbers and values are lists of tuples
        containing error codes and their total downtime, sorted by longest downtime.
    """

    weekly_downtime = defaultdict(lambda: defaultdict(float))
    
    for entry in entries:
        week_number = entry.err_start.isocalendar()[1]
        weekly_downtime[week_number][entry.err_code] += (entry.err_end - entry.err_start).total_seconds() / 60

    return weekly_downtime

def top_5_longest_downtime(weekly_downtime: Dict[int, List[Tuple[str, float]]]) -> Dict[int, List[Tuple[str, float]]]:
    """
    """
    # Prepare the result dictionary with sorted downtimes
    top_5_weekly_downtime = {}

    for week, errors in weekly_downtime.items():
        # Sort the errors by total downtime in descending order and take the top 5
        sorted_errors = sorted(errors.items(), key=lambda x: x[1], reverse=True)[:5]
        top_5_weekly_downtime[week] = sorted_errors
    
    return top_5_weekly_downtime
