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

    def print_temp_hum(self, temp, humidity, display_time):
        message = self.display.message('Temp = {}\nHumidity = {}'.format(temp, humidity))
        wait_clear(display_time)
        return message

    def print_time(self):
        date = str(datetime.datetime.now().date())
        time = str(datetime.datetime.now().time())[0:-7]
        self.display.message('{}\n{}'.format(time, date))
        wait_clear(display_time)

    def print_logo(self):
        self.display.message('FRIDGE MASTER\n    2000')
        wait_clear(display_time)

    def print_pi_info(self):
        CPU_temp = subprocess.check_output(['cat','/sys/class/thermal/thermal_zone0/temp'])
        CPU_temp = str(int(CPU_temp.strip())/1000) + ' C'





    def wait_clear(self, display_time):
        time.sleep(display_time)
        self.display.clear()

lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
lcd.message('Hello!')
