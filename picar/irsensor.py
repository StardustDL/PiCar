import RPi.GPIO as GPIO
import time

_ANA_CS = 5
_ANA_CLOCK = 25
_ANA_ADDRESS = 24
_ANA_DATAOUT = 23
_DIG_LEFT = 16
_DIG_RIGHT = 19


class IRSensor:
    def __init__(self):
        GPIO.setup((_ANA_CS, _ANA_CLOCK, _ANA_ADDRESS), GPIO.OUT)
        GPIO.setup((_ANA_DATAOUT, _DIG_LEFT, _DIG_RIGHT), GPIO.IN, GPIO.PUD_UP)

    def analog(self):
        value = [0] * 6
        for j in range(6):
            GPIO.output(_ANA_CS, GPIO.LOW)
            for i in range(10):
                if i < 4:
                    bit = (((j) >> (3-i)) & 0x01)
                    GPIO.output(_ANA_ADDRESS, bit)
                value[j] <<= 1
                value[j] |= GPIO.input(_ANA_DATAOUT)
                GPIO.output(_ANA_CLOCK, GPIO.HIGH)
                GPIO.output(_ANA_CLOCK, GPIO.LOW)
            GPIO.output(_ANA_CS, GPIO.HIGH)
            time.sleep(0.0001)
        return value[1:]

    def left(self): # 0 for detected
        return GPIO.input(_DIG_LEFT)

    def right(self): # 0 for detected
        return GPIO.input(_DIG_RIGHT)
