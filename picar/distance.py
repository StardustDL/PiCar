import RPi.GPIO as GPIO
import time

_TRIG = 22
_ECHO = 27


class SoundDistance:
    def __init__(self):
        GPIO.setup(_TRIG, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(_ECHO, GPIO.IN)

    def measure(self):
        """
        Wait for 2s at most, return distance in cm, if failed, return None.
        """
        GPIO.output(_TRIG, GPIO.HIGH)
        time.sleep(0.000020)
        GPIO.output(_TRIG, GPIO.LOW)

        cha = GPIO.wait_for_edge(_ECHO, GPIO.RISING, timeout=1000)
        if cha is None:
            return None

        t1 = time.time()

        cha = GPIO.wait_for_edge(_ECHO, GPIO.FALLING, timeout=1000)
        if cha is None:
            return None

        t2 = time.time()

        return (t2-t1)*34000 / 2
