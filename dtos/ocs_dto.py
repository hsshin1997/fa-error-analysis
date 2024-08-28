import os
import glob
import csv
from datetime import datetime

class OhtErrorEntry:
    def __init__(self, eqp_id, online_name, err_start, err_end, keep_up_time, err_code, err_type, err_event, err_text,
                 command_id, cst_id, point, segment, err_station_number, err_station_online_name, err_station_point,
                 from_station, from_station_online_name, to_station, to_station_online_name, order_type, trigger, err_level,
                 user_id, comment):
        self.eqp_id = eqp_id
        self.online_name = online_name
        self.err_start = datetime.strptime(err_start, "%Y-%m-%d %H:%M:%S.%f") if isinstance(err_start, str) else err_start
        self.err_end = datetime.strptime(err_end, "%Y-%m-%d %H:%M:%S.%f") if isinstance(err_end, str) else err_end
        self.keep_up_time = keep_up_time  # This seems to be a duration, so we'll leave it as a string or timedelta
        self.err_code = err_code
        self.err_type = err_type
        self.err_event = err_event
        self.err_text = err_text if err_text else None
        self.command_id = command_id if command_id else None
        self.cst_id = cst_id if cst_id else None
        self.point = point
        self.segment = segment
        self.err_station_number = err_station_number
        self.err_station_online_name = err_station_online_name if err_station_online_name else None
        self.err_station_point = err_station_point
        self.from_station = from_station
        self.from_station_online_name = from_station_online_name if from_station_online_name else None
        self.to_station = to_station
        self.to_station_online_name = to_station_online_name if to_station_online_name else None
        self.order_type = order_type
        self.trigger = trigger
        self.err_level = int(err_level) if err_level else None
        self.user_id = user_id if user_id else None
        self.comment = comment if comment else None

class OhtError:
    def __init__(self):
        self.entries = []

    def add_entry(self, entry: OhtErrorEntry):
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
                        'Number', 'OnlineName', 'OnTime', 'OffTime', 'KeepUpTime', 'ErrCode', 'ErrType', 'ErrEvent', 'ErrText',
                        'CommandID', 'CstID', 'Point', 'Segment', 'ErrStationNumber', 'ErrStationOnlineName', 'ErrStationPoint',
                        'FromStation', 'FromStationOnlineName', 'ToStation', 'ToStationOnlineName', 'OrderType', 'Trigger',
                        'ErrLevel', 'UserID', 'Comment'
                    }
                    if not required_columns.issubset(csv_reader.fieldnames):
                        print(f"Skipping file {file_path}: Missing required columns")
                        continue
                    
                    for row in csv_reader:
                        try:
                            # Extract and clean the fields
                            entry = OhtErrorEntry(
                                eqp_id=row['Number'].strip(),
                                online_name=row['OnlineName'].strip(),
                                err_start=row['OnTime'].strip(),
                                err_end=row['OffTime'].strip(),
                                keep_up_time=row['KeepUpTime'].strip(),
                                err_code=row['ErrCode'].strip(),
                                err_type=row['ErrType'].strip(),
                                err_event=row['ErrEvent'].strip(),
                                err_text=row['ErrText'].strip() if row['ErrText'].strip() else None,
                                command_id=row['CommandID'].strip() if row['CommandID'].strip() else None,
                                cst_id=row['CstID'].strip() if row['CstID'].strip() else None,
                                point=row['Point'].strip(),
                                segment=row['Segment'].strip(),
                                err_station_number=row['ErrStationNumber'].strip(),
                                err_station_online_name=row['ErrStationOnlineName'].strip() if row['ErrStationOnlineName'].strip() else None,
                                err_station_point=row['ErrStationPoint'].strip(),
                                from_station=row['FromStation'].strip(),
                                from_station_online_name=row['FromStationOnlineName'].strip() if row['FromStationOnlineName'].strip() else None,
                                to_station=row['ToStation'].strip(),
                                to_station_online_name=row['ToStationOnlineName'].strip() if row['ToStationOnlineName'].strip() else None,
                                order_type=row['OrderType'].strip(),
                                trigger=row['Trigger'].strip(),
                                err_level=row['ErrLevel'].strip() if row['ErrLevel'].strip() else None,
                                user_id=row['UserID'].strip() if row['UserID'].strip() else None,
                                comment=row['Comment'].strip() if row['Comment'].strip() else None
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
#     oht_error = OhtError()
    
#     # Use '.' to refer to the current directory where the script is located
#     oht_error.read_log_files('.')
    
#     # Accessing entries
#     for entry in oht_error.entries:
#         print(f"Equipment ID: {entry.eqp_id}, Online Name: {entry.online_name}, Error Start: {entry.err_start}, Error End: {entry.err_end}, Keep Up Time: {entry.keep_up_time}, Error Code: {entry.err_code}, Error Type: {entry.err_type}, Error Event: {entry.err_event}, Error Text: {entry.err_text}, Command ID: {entry.command_id}, CST ID: {entry.cst_id}, Point: {entry.point}, Segment: {entry.segment}, Error Station Number: {entry.err_station_number}, Error Station Online Name: {entry.err_station_online_name}, Error Station Point: {entry.err_station_point}, From Station: {entry.from_station}, From Station Online Name: {entry.from_station_online_name}, To Station: {entry.to_station}, To Station Online Name: {entry.to_station_online_name}, Order Type: {entry.order_type}, Trigger: {entry.trigger}, Error Level: {entry.err_level}, User ID: {entry.user_id}, Comment: {entry.comment}")

# if __name__ == "__main__":
#     main()
