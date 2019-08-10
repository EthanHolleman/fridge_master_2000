from DHT_22 import DHT_22
from Door_Sensor import Door_sensor
from Control_Functions import *
from LCD import LCD
from Texter import *
from Logger import *
import RPi.GPIO as GPIO
import time
import datetime
import Adafruit_CharLCD as Ada_LCD

GPIO.setmode(GPIO.BCM)  # set pin labeling scheme DO NOT CHANGE

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
MAX_TEMP = 55  # degrees F
MAX_OPEN = 900  # seconds
FRIDGE_OPEN_CODE = 0
FREEZ_OPEN_CODE = 1
WARN_WAIT = 900  # seconds
WAIT = 5  # seconds

# file directories
LOG_DIR = '/Documents/fridge_master'  # add before running
log_file = os.path.join(LOG_DIR, str(datetime.datetime.now().date()) + '.csv')

# loop variables
last_warning = 0.0
fre_time_open = 0
fri_time_open = 0
loop_counter = 0



while True:
    loop_data = [datetime.datetime.now().date(),
                 datetime.datetime.now().time()]
    fridge, freezer, hum, temp = read_all_sensors(
        fridge_sensor, freezer_sensor, DHT)
    for data in [fridge, freezer, hum, temp]:
        loop_data.append(data)
    print(loop_data)
    # all LCD messages should be included between start_time and difference
    # otherwise door timer will not be accurate
    # currently ignoring non sleep time

    start_time = time.perf_counter()
    lcd.display.clear()
    lcd.display.print_temp_hum(temp, hum, display_time=WAIT)
    lcd.display.print_time(display_time=WAIT)
    lcd.display.print_pi_info(display_time=WAIT)
    #lcs.print_special(WAIT)
    # clear == False so logo remains while rest loop runs
    lcd.display.print_logo(display_time=WAIT, clear=False)
    differnece = time.perf_counter() - start_time  # time for all displays
    # difference is added to open times if state switches is 1 (open)

    fre_time_open, fri_time_open = door_timer(fridge,  # find time doors open
                                              freezer,
                                              fre_time_open,
                                              fri_time_open,
                                              differnece)

    # add open times to loop data
    loop_data.append(fre_time_open)
    loop_data.append(fri_time_open)

    high_temp = temp_monitor(temp, MAX_TEMP)  # check if temp is too high; bool
    left_open, open_code = door_monitor(fre_time_open, fri_time_open, MAX_OPEN)
    # check if doors have been open longer than allowed
    allow_warning = allow_warning(last_warning, WARN_WAIT)  # boolean

    if allow_warning is True:
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
    logger(LOG_DIR, log_file, loop_data)
    # all data collected in loop_data written here
    # current data format for entry
    # date, time, fridge, freezer, hum, temp, fre_time_open, fri_time_open
