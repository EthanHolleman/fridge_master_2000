import RPi.GPIO as GPIO
import Adafruit_DHT

class DHT_22():
    sensor = Adafruit_DHT.DHT22

    def __init__(self, pin):
        self.pin = pin

    def read_temp_hum(self):
        hum, temp = Adafruit_DHT.read_retry(sensor, self.pin)
        if hum is not None and temp is not None:
            return tuple(hum, temp)
        else:
            return False
     
