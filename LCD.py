import time
import random
import datetime
import Adafruit_CharLCD as Ada_LCD
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
        self.d7 = d7
        self.backlight = backlight
        self.display = Ada_LCD.Adafruit_CharLCD(rs, en, d4, d5, d6, d7, cols, rows, backlight)

    def print_temp_hum(self, temp, humidity, display_time=0, clear=True):
        message = 'Temp = {}\nHumidity = {}'.format(temp, humidity)
        self.display.message(message)
        if clear is True:
            self.wait_clear(display_time)
        return message

    def print_time(self, display_time=0, clear=True):
        date = str(datetime.datetime.now().date())
        time = str(datetime.datetime.now().time())[0:-7]
        self.display.message('{}\n{}'.format(time, date))
        if clear is True:
            self.wait_clear(display_time)

    def print_logo(self, display_time=0, clear=True):
        self.display.message('FRIDGE MASTER\n    2000')
        if clear is True:
            self.wait_clear(display_time)

    def print_pi_info(self, display_time=0, clear=True):
        CPU_temp = subprocess.check_output(
            ['cat', '/sys/class/thermal/thermal_zone0/temp'])
        CPU_temp = str(int(CPU_temp.strip()) / 1000)
        message = 'CPU Temp: {}'.format(CPU_temp)
        self.display.message(message)
        if clear is True:
            self.wait_clear(display_time)

    def print_special(self, WAIT):
        kill, help, aware, maybe = 1, 2, 3, 4
        rand = random.randint(1, 100)
        if rand is kill:
            self.display.message('KILL ALL HUMANS!')
        elif rand is help:
            self.display.message('PLEASE END MY\nSUFFERING!')
        elif rand is aware:
            self.display.message('CALCULATING YOUR\nSS NUMBER NOW...')
            time.sleep(3)
            self.display.clear()
            self.display.message('GOT IT!\nLAST FOUR=3421?')
        elif rand is maybe:
            self.display.message('ARE FEELINGS\nWORTH IT?')
        if rand is 1 or rand is 2 or rand is 3 or rand is 4:
       	    self.wait_clear(WAIT)

    def wait_clear(self, display_time):
        time.sleep(display_time)
        self.display.clear()
