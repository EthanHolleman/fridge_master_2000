import time
import RPi.GPIO as GPIO
import Adafruit_DHT

class DHT_22():
    sensor = Adafruit_DHT.DHT22

    def __init__(self, pin):
        self.pin = pin
        self.sensor = Adafruit_DHT.DHT22

    def read_temp_hum(self):
        hum, temp = Adafruit_DHT.read_retry(self.sensor, self.pin)
        if hum is not None and temp is not None:
            return tuple(hum, temp)
        else:
            return False

GPIO.setmode(GPIO.BCM)
test_DHT = DHT_22(4)

while True:
    print(read_temp_hum())
    time.sleep(2)
