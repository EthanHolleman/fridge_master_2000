#!/usr/bin/env python3

import time
import datetime

from Sensors.DHT_22 import DHT_22
from Sensors.Door_Sensor import Door_sensor
from Controls.Control_Functions import *
from Messaging.Texter import *
from Records.Logger import *

from Outputs.LCD import LCD
import Adafruit_CharLCD as Ada_LCD
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)  # set pin labeling scheme PLEASE GOD, DO NOT CHANGE!

# intialize all sensor objects
lcd_rs = 25
lcd_en = 24
lcd_d4 = 23
lcd_d5 = 17
lcd_d6 = 18
lcd_d7 = 22
lcd_backlight = 2
lcd_columns = 16
lcd_rows = 2
lcd = LCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,
          lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

freezer_sensor = Door_sensor(pin_number=21)  # add during wiring
fridge_sensor = Door_sensor(pin_number=5)   # add during wiring
DHT = DHT_22(pin=2)

# sensor constants
MAX_TEMP = 60  # degrees C
MAX_OPEN = 600  # seconds
FRIDGE_OPEN_CODE = 0
FREEZ_OPEN_CODE = 1
WARN_WAIT = 600  # seconds
WAIT = 4  # seconds

# increasing the WAIT is main way of increasing / decreasing the frequency
# that data is written to logs and the length it remains on the LCD

# file directories
LOG_DIR = '/home/pi/FTP/files'  # add before running should be absolute
log_file = os.path.join(LOG_DIR, str(datetime.datetime.now().date()) + '.csv')
# set first log file name as the current date, follows this convention
# for all subsequent logs

# loop variables
last_warning = 0.0
fre_time_open = 0
fri_time_open = 0
loop_counter = 0

while True:
    open_dict = {'fridge': [], 'freezer': []}
    loop_data = [datetime.datetime.now().date(),
                 datetime.datetime.now().time()]

    fridge, freezer, hum, temp = read_all_sensors(
        fridge_sensor, freezer_sensor, DHT)

    append_door_read(open_dict, fridge_sensor, freezer_sensor)

    for data in [fridge, freezer, hum, temp]:
        loop_data.append(data)
    print(loop_data)
    # all LCD messages should be included between start_time and difference
    # otherwise door timer will not be accurate
    # currently ignoring non sleep time

    start_time = time.perf_counter()
    lcd.display.clear()
    lcd.print_temp_hum(temp, hum, display_time=WAIT)
    append_door_read(open_dict, fridge_sensor, freezer_sensor)
    lcd.print_time(display_time=WAIT)
    open_dict = append_door_read(open_dict, fridge_sensor, freezer_sensor)
    lcd.print_pi_info(display_time=WAIT)
    open_dict = append_door_read(open_dict, fridge_sensor, freezer_sensor)
    lcd.print_special(WAIT)
    open_dict = append_door_read(open_dict, fridge_sensor, freezer_sensor)
    # clear == False so logo remains while rest loop runs
    lcd.print_logo(display_time=WAIT, clear=True)
    open_dict = append_door_read(open_dict, fridge_sensor, freezer_sensor)

    differnece = time.perf_counter() - start_time  # time for all displays
    # difference is added to open times if state switches is 1 (open)
    print('The diff is {}'.format(differnece))
    fridge, freezer = read_doors(fridge_sensor, freezer_sensor)

    fre_time_open, fri_time_open = interp_door_dict(fri_time_open,
                                                    fre_time_open,
                                                    open_dict,
                                                    WAIT)

    # add open times to loop data
    loop_data.append(fre_time_open)
    loop_data.append(fri_time_open)

    high_temp = temp_monitor(temp, MAX_TEMP)  # check if temp is too high; bool
    left_open, open_code = door_monitor(fre_time_open, fri_time_open, MAX_OPEN)
    # check if doors have been open longer than allowed
    allow = allow_warning(last_warning, WARN_WAIT)  # boolean
    print('Allow  Warning: {} '.format(allow))
    print('Fridge Open: {} \n Freezer Time Open {}'.format(
        fri_time_open, fre_time_open))

    if allow is True:
        if left_open is True:
            if open_code == 0:
                alarm(fri_alarm=True, open_time=fri_time_open)
            else:
                alarm(fre_alarm=True, open_time=fre_time_open)
            last_warning = time.perf_counter()  # update time of last warning
        if high_temp is True:
            alarm(temp_alarm=True, temp=temp)
            last_warning = time.perf_counter()  # update time of last warning

    loop_counter += 1
    log_file = new_log(LOG_DIR, log_file)
    logger(log_file, loop_data)
    # all data collected in loop_data written here
    # current data format for entry
    # date, time, fridge, freezer, hum, temp, fre_time_open, fri_time_open
