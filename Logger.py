import os
import csv
import datetime

HEADER = ['Date',
          'Time',
          'Fri_Sensor',
          'Fre_Sensor',
          'Humidity',
          'Temp',
          'Fre Time Open',
          'Fri Time Open']


def new_log(log_dir, current_log):
    '''
    Determine if it is a new day and if a new log should be created
    '''

    log_date = current_log.split('.')[0]
    current_day = str(datetime.datetime.now().date())
    print(current_log)
    print(log_date)
    print(current_day)
    print(current_day == log_date)
    if log_date is not current_day:
        new_log = os.path.join(log_dir, current_day + '.csv')
        with open(new_log, 'w+') as new_log:
            writer = csv.writer(new_log, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)
        return new_log
    else:
        return current_log

def check_log_exists(log_dir):
    if os.path.isfile(log_dir) is False:
        with open(log_dir, 'w+') as log:
            writer = csv.writer(log, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(HEADER)


def logger(log_dir, current_log, row):
    '''
    Main logging functionality. Writes entries into the current log file and
    calls new_log to determine if the date has changed and a new log file should
    be created.
    '''
    log_file = new_log(log_dir, current_log)
    try:
        with open(log_file, 'a'):
            writer = csv.writer(log_file, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
    except FileNotFoundError as e:
        return e
