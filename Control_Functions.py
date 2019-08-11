import datetime
import subprocess
import time
from Texter import *


def read_all_sensors(fridge_sensor, freezer_sensor, DHT):
    fridge_state = fridge_sensor.get_state()
    freezer_state = freezer_sensor.get_state()
    humidity, temp = DHT.read_temp_hum()

    return tuple([fridge_state, freezer_state, humidity, temp])


def door_timer(fridge_state, freezer_state, fri_open, fre_open, time):
    if fridge_state is 1:
        fri_open += time
    else:
        fri_open = 0
    if freezer_state is 1:  # change from open to open output
        fre_open += time
    else:
        fre_open = 0

    return tuple([fre_open, fri_open])


def door_monitor(fre_open, fri_open, max_open_time):
    if fre_open > max_open_time:
        return tuple([True, 1])
    elif fri_open > max_open_time:
        return tuple([True, 0])
    else:
        return tuple([False, None])


def temp_monitor(temp, allowed_max_temp):
    if float(temp) > allowed_max_temp:
        return True
    else:
        return False


def allow_warning(last_warning, wait_time):
    current_time = time.perf_counter()
    time_since_warning = current_time - last_warning

    if time_since_warning > wait_time:
        return True
    else:
        return False


def alarm(fre_alarm=False, fri_alarm=False, temp_alarm=False, temp=None, open_time=None):
    pending_alarms = ''
    if fre_alarm is True:
        pending_alarms = compose_warnings(emergency_freezer=True, open_time=open_time)
    elif fri_alarm is True:
        pending_alarms = compose_warnings(emergency_fridge=True,
                                          open_time=open_time)
    elif temp_alarm is True:
        pending_alarms = compose_warnings(emergency_temp=True, temp=temp)

    send_warnings(pending_alarms, get_client())

    return pending_alarms
