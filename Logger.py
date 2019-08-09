import os
import csv
import datetime


def write_entry(data_list, log_path):
    try:
        with open(log_path, 'a') as log:
            writer = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(data_list)
    except FileNotFoundError as e:
        return e


def new_log(log_dir, current_log):
    '''
    Determine if it is a new day and if a new log should be created
    '''
    # need to edit header contents

    HEADER = ['Date',
              'Time',
              'Fri_Sensor',
              'Fre_Sensor',
              'Humidity',
              'Temp',
              'Fre Time Open',
              'Fri Time Open']

    log_date = current_log.split('.')[0]
    current_day = datetime.datetime.now().date()

    if log_date is not current_day:
        new_log = os.path.join(log_dir, current_day + '.csv')
        with open(new_log, 'w'):
            writer = csv.writer(new_log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
        return new_log
    else:
        return current_log


def logger(log_dir, current_log, row):
    log_file = new_log(log_dir, current_log)
    try:
        with open(log_file, 'a'):
            writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
    except FileNotFoundError as e:
        return e
