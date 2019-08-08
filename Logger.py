import os
import csv
import datetime
LOG_NAME = 'Fridge_Log.csv'

def check_for_log(log_path):
    if os.path.exists(log_path):
        return True
    else:
        header = ['Date', 'Temp', 'Humidity', 'Allow_warning', 'Warning', 'Fridge', 'Freezer']
        with open(LOG_NAME, 'w') as log:
            writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            write.writerow(header)

def write_entry(data_list):
    try:
        with open(log_path, 'a') as log:
            writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data_list)
    except FileNotFoundError as e:
        return e
