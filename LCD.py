import time
import datetime
import Adafruit_CharLCD as LCD
import subprocess


class LCD():

    def __init__(self, rs, en, d4, d5, d6, d7, cols, rows, backlight):
        self.cols = cols
        self.rows = rows
        self.rs = rs
        self.en = en
        self.d4 = d4
        self.d5 = d5
        self.d6 = d6
        self.d7= d7
        self.backlight = backlight
        self.display = LCD(self, rs, en, d4, d5, d6, d7, cols, rows, backlight)

    def print_temp_hum(self, temp, humidity, display_time=0, clear=False):
        message = self.display.message('Temp = {}\nHumidity = {}'.format(temp, humidity))
        if clear is True: wait_clear(display_time)
        return message

    def print_time(self, display_time=0, clear=False):
        date = str(datetime.datetime.now().date())
        time = str(datetime.datetime.now().time())[0:-7]
        self.display.message('{}\n{}'.format(time, date))
        if clear is True: wait_clear(display_time)

    def print_logo(self, display_time=0, clear=False):
        self.display.message('FRIDGE MASTER\n    2000')
        if clear is True: wait_clear(display_time)

    def print_pi_info(self, display_time=0, clear=False):
        CPU_temp = subprocess.check_output(['cat','/sys/class/thermal/thermal_zone0/temp'])
        CPU_temp = str(int(CPU_temp.strip())/1000)
        GPU_temp = subprocess.check_output(['vcgencmd', 'measure_temp'])[5:9]

        message = 'CPU Temp: {}C\nGPU Temp: {}C'.format(CPU_temp, GPU_temp)
        self.display(message)
        if clear is True: wait_clear(display_time)

    def wait_clear(self, display_time):
        time.sleep(display_time)
        self.display.clear()
