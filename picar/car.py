from . import init
from . import joystick
from . import servo
from . import led
from . import irremote
from . import irsensor
from . import motor
from . import distance
from .irremote import Key
import threading
import time


class Car:
    def __init__(self):
        init.init()
        self.joystick = joystick.Joystick()
        self.led = led.LedManager()
        self.distance = distance.SoundDistance()
        self.irremote = irremote.IRRemote()
        self.irsensor = irsensor.IRSensor()
        self.motorA = motor.getMotorA()
        self.motorB = motor.getMotorB()
        # self.servo = servo.ServoManager()
        self.motors = (self.motorA, self.motorB)

    def run(self, speed=10, direction=None):
        speed = min(99, max(0, speed))
        for motor in self.motors:
            if direction is not None:
                motor.direction = direction
            motor.speed = speed

    def wait(self):
        self.run(speed=0)

    def left(self, speed=10):
        self.run(0, 0)
        self.motorA.direction = 1
        self.run(speed=speed)

    def right(self, speed=10):
        self.run(0, 0)
        self.motorB.direction = 1
        self.run(speed=speed)

    def __del__(self):
        del self.joystick
        del self.led
        del self.distance
        del self.irremote
        del self.irsensor
        del self.motorA
        del self.motorB
        # del self.servo
        init.cleanup()

    def runByRemote(self, speed=10):
        speed = min(99, max(0, speed))
        origin = speed
        while True:
            key = self.irremote.recieve()
            if key is Key.Num2:
                self.run(direction=0, speed=speed)
            elif key is Key.Num8:
                self.run(direction=1, speed=speed)
            elif key is Key.Num5:
                self.wait()
            elif key is Key.Num4:
                self.left(speed=speed)
            elif key is Key.Num6:
                self.right(speed=speed)
            elif key is Key.Minus:
                speed = max(0, speed - 10)
                self.run(speed=speed)
            elif key is Key.Plus:
                speed = min(99, speed + 10)
                self.run(speed=speed)
            elif key is Key.EQ:
                speed = origin
                self.run(speed=speed)
