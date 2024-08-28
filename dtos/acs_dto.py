import os
import glob
import csv
from datetime import datetime

class AgvErrorEntry:
    def __init__(self, err_start, err_end, eqp_type, eqp_id, start_pos, end_pos, current_job, current_pos, err_code, err_level):
        self.err_start = err_start  # Assuming this is in a time format, not full datetime
        self.err_end = err_end  # Assuming this is in a time format, not full datetime
        self.eqp_type = eqp_type
        self.eqp_id = eqp_id
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.current_job = current_job
        self.current_pos = current_pos
        self.err_code = err_code
        self.err_level = int(err_level)

class AgvError:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: AgvErrorEntry):
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
                with open(file_path, mode='r', encoding='utf-8') as file:  # Use UTF-8 encoding to read Korean characters
                    csv_reader = csv.DictReader(file)

                    # Check if the CSV file has the required columns
                    required_columns = {
                        'Occur Time', 'Finish Time', 'Equipments Type', 'Equipments ID',
                        'Start Position', 'End Position', 'Now Operation', 'Now Position',
                        'Error Code', 'Error Level'
                    }
                    if not required_columns.issubset(csv_reader.fieldnames):
                        print(f"Skipping file {file_path}: Missing required columns")
                        continue
                    
                    for row in csv_reader:
                        try:
                            # Extract and clean the fields
                            err_start = row['Occur Time'].strip()  # Updated from occur_time to err_start
                            err_end = row['Finish Time'].strip()  # Updated from finish_time to err_end
                            eqp_type = row['Equipments Type'].strip()  # Updated from eq_type to eqp_type
                            eqp_id = row['Equipments ID'].strip()  # Updated from eq_id to eqp_id
                            start_pos = row['Start Position'].strip()
                            end_pos = row['End Position'].strip()
                            current_job = row['Now Operation'].strip()  # Updated from now_op to current_job
                            current_pos = row['Now Position'].strip()  # Updated from now_pos to current_pos
                            err_code = row['Error Code'].strip()
                            err_level = row['Error Level'].strip()

                            # Create AgvErrorEntry and add it to entries
                            entry = AgvErrorEntry(
                                err_start=err_start,
                                err_end=err_end,
                                eqp_type=eqp_type,
                                eqp_id=eqp_id,
                                start_pos=start_pos,
                                end_pos=end_pos,
                                current_job=current_job,
                                current_pos=current_pos,
                                err_code=err_code,
                                err_level=err_level
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
#     agv_error = AgvError()
    
#     # Use '.' to refer to the current directory where the script is located
#     agv_error.read_log_files('.')
    
#     # Accessing entries
#     for entry in agv_error.entries:
#         print(f"Error Start: {entry.err_start}, Error End: {entry.err_end}, Equipment Type: {entry.eqp_type}, Equipment ID: {entry.eqp_id}, Start Position: {entry.start_pos}, End Position: {entry.end_pos}, Current Job: {entry.current_job}, Current Position: {entry.current_pos}, Error Code: {entry.err_code}, Error Level: {entry.err_level}")

# if __name__ == "__main__":
#     main()
