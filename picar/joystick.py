import RPi.GPIO as GPIO
import time
from enum import Enum

class StickType(Enum):
    Center = 7
    Front = 8
    Right = 9
    Left = 10
    Back = 11


class Joystick:
    def __init__(self):
        self.callback = None
        for pin in StickType:
            GPIO.setup(pin.value, GPIO.IN, GPIO.PUD_UP)
            GPIO.add_event_detect(pin.value, GPIO.FALLING, callback=self._callback)

    def _callback(self, channel):
        if self.callback:
            self.callback(StickType(channel))


