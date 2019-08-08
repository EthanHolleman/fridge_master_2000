import RPi.GPIO as GPIO
import signal

class Door_sensor:

    NUM_PINS = 2

    def __init__(self, pin_number):
        self.pin_number = pin_number
        GPIO.setup(self.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def get_state(self):
    	return GPIO.input(self.pin_number)
