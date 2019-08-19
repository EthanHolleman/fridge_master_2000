import datetime
import os
import csv


def get_log_column(log_path, column_header):
    try:
        data = []
        with open(log_path, 'r'):
            reader = csv.DictReader(log_path)
            for row in reader:
                data.append(row[column_header])
        return data
    except FileNotFoundError as e:
        return e

def get_log_columns(log_path, *args):
    data_dick = dict(zip(args, [[] for i in range(0, len(args))]))
    try:
        with open(log_path, 'r'):
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
    previous_date = datetime.date.today()-datetime.timedelta(1)
    return os.path.join(log_dir, str(previous_date) + '.csv')


def yesterday_high_temp(log_dir, temp_header):
    temp_data = get_log_column(get_yesterday_log(log_dir), temp_header)
    if temp_data is not FileNotFoundError:
        temp_data = [float(x) for x in temp_data]
        return str(max(temp_data))
    else:
        return 'LOG NOT FOUND'


def yesterday_opens(log_dir, open_headers_list):
    # number of opens are returned based on the order of the headers given
    # if fridge opens header is provided first in list it will be returned
    # as the first value in the tuple.
    previous_log = get_yesterday_log(log_dir)
    data = get_log_columns(previous_log, open_headers_list)
    if data is not FileNotFoundError:
        sums = [sum(data[key]) for key in data]
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
    
