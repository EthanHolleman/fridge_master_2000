import time
import RPi.GPIO as GPIO
import Adafruit_DHT

class DHT_22():

    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22

    def read_temp_hum(self):
        hum, temp = Adafruit_DHT.read_retry(self.sensor, self.pin)
        temp = str(temp)[0:4]
        hum = str(hum)[0:4]
        if hum is not None and temp is not None:
                return tuple([hum, temp])
        else:
                return False

    def convert_to_F(self, temp):
        return (temp * 1.8) + 32
