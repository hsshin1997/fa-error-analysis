from dtos import StackerCraneError
from analysis import longestDowntime


def main():
    file_path = []
    
    # StackerCraneNames = ['Reel-Anode', 'Reel-Cathode', 'Pre-VD-Anode', 'Post-VD-Anode', 'Pre-VD-Cathode', 'Post-VD-Cathode']
    # AGVNames = ['VD-Anode', 'VD-Cathode', 'Stacking']
    # OHTNames = ['Notching']
    # ConveyorNames = [] 

    # for name in StackerCraneNames: 
    #     file_path.append(f'./data/stacker_crane/{name}.csv')


    scs_error = StackerCraneError()
    scs_error.read_log_files('./data/w34/scs/reel-an/E0STKA51.csv')

    weekly_down_time = longestDowntime(scs_error.entries)
    # for entry in scs_error.entries:
    #     print(f"Equipment ID: {entry.eqp_id}, Unit ID: {entry.unit_id}, Error Code: {entry.error_code}, Error Message: {entry.err_msg}, Barcode ID: {entry.bcd_id}, Start: {entry.err_start}, End: {entry.err_end}")


    # # Example usage

if __name__ == "__main__":
    main()



