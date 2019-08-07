import RPi.GPIO as GPIO
import signal

class Door_sensor:

    NUM_PINS = 2

    def __init__(self, pin_number):
        self.pin_number = pin_number

        def setup(self):
            GPIO.setup(self.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        def get_state():
            return GPIO.input(self.pin_number)
            
GPIO.setmode(GPIO.BCM)
door_test = Door_sensor(pin_number=18)
door_test.setup()
print(door_test.get_state())
