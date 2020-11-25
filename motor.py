import RPi.GPIO as GPIO
import time

class Motor:
    def __init__(self, a, b, control):
        self.a = a
        self.b = b
        self.control = control
        GPIO.setup((self.a, self.b, self.control), GPIO.OUT)
        self.pwm = GPIO.PWM(self.control, 1000)
        self.pwm.start(0)
        self.direction = 1
        self.speed = 0

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value
        if value == 0:
            GPIO.output((self.a, self.b), (0, 1))
        else:
            GPIO.output((self.a, self.b), (1, 0))
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        if 0 <= value <= 100:
            self._speed = value
            self.pwm.ChangeDutyCycle(self._speed)
        else:
            raise Exception(f"Speed should be in [0, 100], but got {value}")

    def __del__(self):
        self.pwm.stop()

def getMotorA():
    _A = Motor(12, 13, 6)
    return _A

def getMotorB():
    _B = Motor(20, 21, 26)
    return _B

