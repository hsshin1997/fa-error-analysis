import os
import glob
import csv
from datetime import datetime

class ConveyorErrorEntry:
    def __init__(self, eqp_id, unit_id, err_code, err_msg, bcd_id, err_start, err_end):
        self.eqp_id = eqp_id
        self.unit_id = unit_id
        self.err_code = err_code
        self.err_msg = err_msg if err_msg else None  # Handle missing error messages
        self.bcd_id = bcd_id if bcd_id else None  # Handle missing barcode IDs
        self.err_start = datetime.strptime(err_start, "%m/%d/%Y %I:%M:%S %p") if isinstance(err_start, str) else err_start
        self.err_end = datetime.strptime(err_end, "%m/%d/%Y %I:%M:%S %p") if isinstance(err_end, str) else err_end

class ConveyorError:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: ConveyorErrorEntry):
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
                with open(file_path, mode='r', encoding='utf-8') as file:  # Use UTF-8 encoding to read non-ASCII characters
                    csv_reader = csv.DictReader(file)

                    # Check if the CSV file has the required columns
                    required_columns = {
                        'EQP ID', 'UNIT ID', 'Error Code', 'Error Message', 'BARCODE ID', 'ERR START DTTM', 'ERR END DTTM'
                    }
                    if not required_columns.issubset(csv_reader.fieldnames):
                        print(f"Skipping file {file_path}: Missing required columns")
                        continue
                    
                    for row in csv_reader:
                        try:
                            # Extract and clean the fields
                            eqp_id = row['EQP ID'].strip()
                            unit_id = row['UNIT ID'].strip()
                            err_code = row['Error Code'].strip()
                            err_msg = row['Error Message'].strip() if row['Error Message'].strip() else None
                            bcd_id = row['BARCODE ID'].strip() if row['BARCODE ID'].strip() else None
                            err_start = row['ERR START DTTM'].strip()
                            err_end = row['ERR END DTTM'].strip()

                            # Create ConveyorErrorEntry and add it to entries
                            entry = ConveyorErrorEntry(
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

# Example usage
# def main():
#     conveyor_error = ConveyorError()
    
#     # Use '.' to refer to the current directory where the script is located
#     conveyor_error.read_log_files('.')
    
#     # Accessing entries
#     for entry in conveyor_error.entries:
#         print(f"Equipment ID: {entry.eqp_id}, Unit ID: {entry.unit_id}, Error Code: {entry.err_code}, Error Message: {entry.err_msg}, Barcode ID: {entry.bcd_id}, Error Start: {entry.err_start}, Error End: {entry.err_end}")

# if __name__ == "__main__":
#     main()
