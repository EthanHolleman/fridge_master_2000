from DHT_22 import DHT_22
from Door_Sensor import Door_sensor
from Control_Functions import *
from Texter import *
from Logger import *
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BCM)  # set pin labeling scheme DO NOT CHANGE

# intialize all sensor objects
freezer_sensor = Door_sensor(pin_number=)
fridge_sensor = Door_sensor(pin_number=)
DHT = DHT_22(pin=)
lcd = LCD()

# sensor constants
MAX_TEMP = 55  # degrees F
MAX_OPEN = 900  # seconds
FRIDGE_OPEN_CODE = 0
FREEZ_OPEN_CODE = 1
WARN_WAIT = 900  # seconds
WAIT = 5  # seconds

# file directories
LOG_DIR = ''  # add before running
log_file = os.path.join(LOG_DIR, datetime.datetime.now().date() + '.csv')

# loop variables
last_warning = 0.0
fre_time_open = 0
fri_time_open = 0
loop_counter = 0

while True:
    loop_data = [datetime.datetime.now().date(), datetime.datetime.now().time()]
    fridge, freezer, hum, temp = read_all_sensors(fridge_sensor, freezer_sensor, DHT)

    loop_data.append(fridge, freezer, hum, temp)
    # all LCD messages should be included between start_time and difference
    # otherwise door timer will not be accurate
    # currently ignoring non sleep time

    start_time = time.perf_counter()
    lcd.clear()
    lcd.print_temp_hum(temp, hum, display_time=WAIT)
    lcd.print_time(display_time=WAIT)
    lcd.print_pi_info(display_time=WAIT)
    lcd.print_logo(display_time=WAIT, clear=False)  # clear == False so logo remains while rest loop runs
    differnece = time.perf_counter() - start_time  # time for all displays to happen
    # difference is added to open times if state switches is 1 (open)

    fre_time_open, fri_time_open = door_timer(fridge,  # calculate time doors have been open
                                              freezer,
                                              fre_time_open,
                                              fri_time_open,
                                              differnece)

    loop_data.append(fre_time_open, fri_time_open)  # add open times to loop data

    high_temp = temp_monitor(temp, MAX_TEMP)  # check if temp is too high; bool
    left_open, open_code = door_monitor(fre_time_open, fri_time_open, MAX_OPEN)
    # check if doors have been open longer than allowed
    allow_warning = allow_warning(last_warning, WARN_WAIT)  # boolean

    if allow_warning is True:
        if left_open is True
            if open_code == 0:
                alarm(fri_alarm=True, open_time=fri_time_open)
            else:
                alarm(fre_alarm=True, open_time=fre_time_open)
            last_warning = time.perf_counter()  # update time of last warning
        if high_temp is True:
            alarm(temp_alarm=True, temp=temp)
            last_warning = time.perf_counter()  # update time of last warning

    loop_counter += 1
    logger(LOG_DIR, log_file, loop_data)
    # all data collected in loop_data written here
    # current data format for entry
    # date, time, fridge, freezer, hum, temp, fre_time_open, fri_time_open
