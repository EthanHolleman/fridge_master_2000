import time
import random
import datetime
import subprocess
import Adafruit_CharLCD as Ada_LCD

from Controls.Control_Functions import c_to_f
from Stats.Stats import yesterday_high_temp
from Stats.Stats import yesterday_opens


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
        self.display = Ada_LCD.Adafruit_CharLCD(
            rs, en, d4, d5, d6, d7, cols, rows, backlight)

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
        CPU_temp = str(c_to_f(int(CPU_temp.strip()) / 1000))
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

    def print_yesterday_high(self,
                             temp_header,
                             log_dir,
                             display_time=0,
                             clear=True):
        high_temp = yesterday_high_temp(log_dir, temp_header)
        self.display.message('Yesterday High\n{} F'.format(high_temp))
        if clear is True:
            self.wait_clear(display_time)

    def print_yesterday_opens(self,
                              open_headers_list,
                              log_dir,
                              display_time=0,
                              clear=True):

        fre_opens, fri_opens = (yesterday_opens(log_dir, open_headers_list))
        self.display.message('# Fridge Opens\nYesterday: {}'.format(fri_opens))
        time.sleep(3)
        self.display.clear()
        self.display.message('# Freezer Opens\nYesterday: {}'.format(fre_opens))
        if clear is True:
            self.wait_clear(display_time)
            
    def print_lifetime_opens():
        pass

    def wait_clear(self, display_time):
        time.sleep(display_time)
        self.display.clear()

    def print_all_stats(self,
                        temp_header,
                        open_headers_list,
                        log_dir,
                        display_time=0,
                        clear=True):
        pass
