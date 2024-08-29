from dtos import StackerCraneError
from analysis import *

from typing import List, Dict, Tuple
# from analysis import longestDowntime

def print_weekly_downtime_report(weekly_downtime: Dict[int, List[Tuple[str, float]]]):
    """
    Print a report of the top 5 longest total downtimes for each week.
    
    Args:
        weekly_downtime: A dictionary returned by calculate_weekly_downtime.
    """
    for week, errors in sorted(weekly_downtime.items()):
        print(f"\nWeek {week}:")
        for err_code, downtime in errors:
            print(f"  Error Code: {err_code}, Total Downtime: {downtime / 3600:.2f} hours")


def main():
    file_path = []
    
    # StackerCraneNames = ['Reel-Anode', 'Reel-Cathode', 'Pre-VD-Anode', 'Post-VD-Anode', 'Pre-VD-Cathode', 'Post-VD-Cathode']
    # AGVNames = ['VD-Anode', 'VD-Cathode', 'Stacking']
    # OHTNames = ['Notching']
    # ConveyorNames = [] 

    # for name in StackerCraneNames: 
    #     file_path.append(f'./data/stacker_crane/{name}.csv')


    scs_error = StackerCraneError()
    scs_error.read_log_files('data/w34/scs/vd-an') #data\w34\scs\reel-an\E0STKA51.csv
    # for entry in scs_error.entries:
    #     print(f"Equipment ID: {entry.eqp_id}, Unit ID: {entry.unit_id}, Error Code: {entry.err_code}, Error Message: {entry.err_msg}, Barcode ID: {entry.bcd_id}, Start: {entry.err_start}, End: {entry.err_end}")

    # Downtime sum
    weekly_downtime = calculate_weekly_downtime(scs_error.entries)
    top5 = top_5_longest_downtime(weekly_downtime)
    print(top5)

    # Error Occurene Count
    occurrence_by_error_code = occurence_count(scs_error.entries)
    top5 = most_frequent_errors(occurrence_by_error_code, 5)
    print(top5)

    # # Example usage

if __name__ == "__main__":
    main()



