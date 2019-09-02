import datetime
import os
import csv


def get_log_column(log_path, column_header):
    '''
    Given the log path and a header returns a list of the data in the column
    identified to that header.
    '''
    try:
        data = []
        with open(log_path) as log_path:
            reader = csv.DictReader(log_path)
            for row in reader:
                data.append(row[column_header])

        return data
    except FileNotFoundError as e:
        return e



def get_log_columns(log_path, *args):
    '''
    Same idea as get_log_column but is able to return column for as many headers
    as there are in the cscv file being read. Returns a dictionary of lists,
    where keys are the headers and lists contain data under those headers.
    '''
    data_dick = dict(zip(args, [[] for i in range(0, len(args))]))
    try:
        with open(log_path, 'r') as log_path:
            reader = csv.DictReader(log_path)
            for row in reader:
                for key in data_dick:
                    data_dick[str(key)].append(row[key])
                    # append values at each header to the dictionary under their
                    # key which is the that header
        return data_dick
    except FileNotFoundError as e:
        return e


def get_yesterday_log(log_dir):
    '''
    Given the directory where log files are stored, returns the path to log file
    that would have been created on the previous day. Does not currently check
    if that log file actually exists. This is doen in other functions.
    '''
    previous_date = datetime.date.today()-datetime.timedelta(1)
    return os.path.join(log_dir, str(previous_date) + '.csv')


def yesterday_high_temp(log_dir, temp_header):
    '''
    Returns the recorded high temp from the log file recorded on the previous
    date. If that file does not exist returns string warning that can be printed
    to the LCD.
    '''
    temp_data = get_log_column(get_yesterday_log(log_dir), temp_header)
    if temp_data is not FileNotFoundError:
        temp_data = [float(x) for x in temp_data]
        return str(max(temp_data))
    else:
        return 'LOG NOT FOUND'


def yesterday_opens(log_dir, *args):
    # number of opens are returned based on the order of the headers given
    # if fridge opens header is provided first in list it will be returned
    # as the first value in the tuple.

    # idea that you use the name of the current log to get the previous one
    previous_log = get_yesterday_log(log_dir)
    print(previous_log)
    print('--------------------------')
    data = get_log_columns(previous_log, *args)
    if data is not FileNotFoundError:
        sums = [sum(int(x) for x in data[key]) for key in data]
        return tuple(sums)
    else:
        return tuple(['LOG NOT FOUND', 'LOG NOT FOUND'])
    # if error log not found messages returned in LCD printable format so
    # the messages can be displayed on screen without terminating the
    # main loop

def get_lifetime_opens():
    pass
    # return dictionary with date from logfile name and number times freezer
    # and fridge has been opened


def get_lifetime_opens_high():
    pass
    '''
    Use the output of get_lifetime_opens to find the day with the greatest
    number of Opens
    '''
