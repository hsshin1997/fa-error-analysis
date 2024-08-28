import os
import glob
import csv
from datetime import datetime

class StackerCraneErrorEntry:
    def __init__(self, eqp_id, unit_id, err_code, err_msg, bcd_id, err_start, err_end):
        self.eqp_id = eqp_id
        self.unit_id = unit_id
        self.err_code = err_code
        self.err_msg = err_msg
        self.bcd_id = bcd_id if bcd_id else None  # Set to None if bcd_id is blank
        self.err_start = datetime.strptime(err_start, "%Y-%m-%d %H:%M:%S") if isinstance(err_start, str) else err_start
        self.err_end = datetime.strptime(err_end, "%Y-%m-%d %H:%M:%S") if isinstance(err_end, str) else err_end

class StackerCraneError:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: StackerCraneErrorEntry):
        self.entries.append(entry)

    def read_log_files(self, folder_path: str):
        # Find all CSV files in the given folder
        csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

        # Check if no CSV files are found
        if not csv_files:
            print(f"No CSV files found in folder: {folder_path}")
            return
        
        # Iterate over each CSV file found in the folder
        for file_path in csv_files:
            try:
                with open(file_path, mode='r') as file:
                    csv_reader = csv.DictReader(file)

                    # Check if the CSV file has the required columns
                    required_columns = {
                        'EQP_ID', 'UNIT_ID', 'ERR_CD', 'ERR_MSG',
                        'BARCODE_ID', 'ERR_START_DTTM', 'ERR_END_DTTM'
                    }
                    if not required_columns.issubset(csv_reader.fieldnames):
                        print(f"Skipping file {file_path}: Missing required columns")
                        continue
                    
                    for row in csv_reader:
                        try:
                            # Extract and clean the fields, handling empty BARCODE_ID
                            eqp_id = row['EQP_ID'].strip()
                            unit_id = row['UNIT_ID'].strip()
                            err_code = row['ERR_CD'].strip()
                            err_msg = row['ERR_MSG'].strip()
                            bcd_id = row['BARCODE_ID'].strip() if row['BARCODE_ID'].strip() else None
                            err_start = row['ERR_START_DTTM'].strip()
                            err_end = row['ERR_END_DTTM'].strip()

                            # Create ScsErrorEntry and add it to entries
                            entry = StackerCraneErrorEntry(
                                eqp_id=eqp_id,
                                unit_id=unit_id,
                                err_code=err_code,
                                err_msg=err_msg,
                                bcd_id=bcd_id,
                                err_start=err_start,
                                err_end=err_end
                            )
                            self.add_entry(entry)
                        except KeyError as e:
                            print(f"Missing data in row: {row}. Error: {e}")
                        except ValueError as e:
                            print(f"Invalid data format in row: {row}. Error: {e}")
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except IOError as e:
                print(f"IO error occurred while reading file {file_path}: {e}")

# # Example usage
# def main():
#     scs_error = ScsError()
    
#     # Use '.' to refer to the current directory where the script is located
#     scs_error.read_log_files('.')
    
#     # Accessing entries
#     for entry in scs_error.entries:
#         print(f"Equipment ID: {entry.eqp_id}, Unit ID: {entry.unit_id}, Error Code: {entry.error_code}, Error Message: {entry.err_msg}, Barcode ID: {entry.bcd_id}, Start: {entry.err_start}, End: {entry.err_end}")

# if __name__ == "__main__":
#     main()
