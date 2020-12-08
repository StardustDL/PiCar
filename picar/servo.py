import Adafruit_PCA9685


class Servo:
    def __init__(self, manager, index):
        self.manager = manager
        self.index = index
        self._angle = None

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.manager.apply(self.index, self._angle)


class ServoManager:
    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.servo0 = Servo(self, 0)
        self.servo1 = Servo(self, 1)

    def apply(self, index, angle):
        value = 4095 * (angle * 11 + 500) / 20000
        self.pwm.set_pwm(index, 0, int(value))
