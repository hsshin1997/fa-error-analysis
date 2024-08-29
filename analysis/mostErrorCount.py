from collections import defaultdict
from datetime import datetime, timedelta
from typing import List, Tuple, Any

def occurence_count(entries: List) -> dict:
    """Return the occurence count of each error."""
    occurrence_by_error_code = defaultdict(int)
    
    for entry in entries:
        occurrence_by_error_code[entry.err_code] += 1
    
    return occurrence_by_error_code

def most_frequent_errors(entries: dict, n: int) -> List[Tuple[str, int]]:
    """Return the n most frequent errors."""
    top_n_errors = sorted(entries.items(), key=lambda x: x[1], reverse=True)[:n]
    return top_n_errors


# def top_5_most_frequent_errors(entries: List) -> List[Tuple[str, int]]:
#     """Return the top 5 errors that occurred most frequently."""
#     occurrence_by_error_code = defaultdict(int)
    
#     for entry in entries:
#         occurrence_by_error_code[entry.err_code] += 1
    
#     top_5_errors = sorted(occurrence_by_error_code.items(), key=lambda x: x[1], reverse=True)[:5]
#     return top_5_errors