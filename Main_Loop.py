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

SLEEP_TIME = 5
open_times = [0,0]
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
    if temp <= 60:
        # send text message warning






    humidity, temp = DHT.read_temp_hum()
