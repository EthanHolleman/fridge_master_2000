from DHT_22 import DHT_22
from Door_Sensor import Door_sensor
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BMC)
# intialize all sensor objects
freezer_sensor = Door_sensor(pin_number=)
fridge_sensor = Door_sensor(pin_number=)
DHT = DHT_22(pin=)

# setup door sensors
freezer_sensor.setup()
fridge_sensor.setup()


'''
Features to add
Send text message once door has been closed after warning
Cool down on warning messages 10 mins or sor
'''

SLEEP_TIME = 5
open_times = [0,0]
last_warning = 0.0
warning_wait_seconds = 900
allowed_temp = 60
allowed_open = 900
while True():

    # read from all sensors
    fridge_state = fridge_sensor.get_state()
    freezer_state = freezer_state.get_state()
    time.sleep(SLEEP_TIME)

    if frige_state is open:
        open_times[0] += SLEEP_TIME
    else:
        open_times[0] = 0
    if freezer_state is open: # change from open to open output
        open_times[1] += SLEEP_TIME
    else:
        open_times[1] = 0

    humidity, temp = DHT.read_temp_hum()
    time_since_last_warning = time.perf_counter-last_warning
    allow_warning = time_since_last_warning >= warning_wait_seconds

    if allow_warning is True:
        if temp >= allowed_temp:
            # send message and log
            pass
        if open_times[0] >= allowed_open:
            # send message
            pass
        if open_times[1] >= allowed_open:
            # send message
            pass
