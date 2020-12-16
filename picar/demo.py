import random
import os
from . import irremote
from . import car
from . import server

class FakeLed:
    def __init__(self):
        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255), 255)


class FakeLeds:
    def __init__(self):
        self.brightness = 128
        self.leds = [FakeLed() for _ in range(4)]


class FakeIRSensor:
    def left(self):
        return random.randint(0, 1)

    def right(self):
        return random.randint(0, 1)

    def analog(self):
        return random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000), random.randint(0, 1000)


class FakeIRRemote:
    def recieve(self):
        return random.choice(list(irremote.Key))


class FakeMotor:
    def __init__(self):
        self.speed = random.randint(0, 99)
        self.direction = random.randint(0, 1)


class FakeCar:
    def __init__(self):
        self.led = FakeLeds()
        self.irsensor = FakeIRSensor()
        self.motorA = FakeMotor()
        self.motorB = FakeMotor()
        self.irremote = FakeIRRemote()
        self.motors = (self.motorA, self.motorB)
        self.controller_ir = None
        self.controller_st = None
        self.controller_oa = None

    def start_controller_ir(self, speed=10):
        if self.controller_ir is not None:
            return
        self.controller_ir = car.CarController(
            self, car.infraredRemoteController, speed=speed)
        self.controller_ir.run()

    def stop_controller_ir(self):
        if self.controller_ir is None:
            return
        self.controller_ir.shutdown()
        self.controller_ir = None

    def start_controller_oa(self, speed=20, interval=0.3):
        if self.controller_oa is not None:
            return
        self.controller_oa = car.CarController(
            self, car.obstacleAvoidanceController, speed=speed, interval=interval)
        self.controller_oa.run()

    def stop_controller_oa(self):
        if self.controller_oa is None:
            return
        self.controller_oa.shutdown()
        self.controller_oa = None

    def start_controller_st(self, speed=5, interval=0.1):
        if self.controller_st is not None:
            return
        self.controller_st = car.CarController(
            self, car.selfTraceController, speed=speed, interval=interval)
        self.controller_st.run()

    def stop_controller_st(self):
        if self.controller_st is None:
            return
        self.controller_st.shutdown()
        self.controller_st = None

    def line(self, speed=10, direction=None):
        speed = min(99, max(0, speed))
        for motor in self.motors:
            if direction is not None:
                motor.direction = direction
            motor.speed = speed

    def stop(self):
        self.line(speed=0)

    def fore(self, speed=10):
        self.line(direction=0, speed=speed)

    def back(self, speed=10):
        self.line(direction=1, speed=speed)

    def left(self, speed=10):
        self.line(0, 0)
        self.motorA.direction = 1
        self.line(speed=speed)

    def right(self, speed=10):
        self.line(0, 0)
        self.motorB.direction = 1
        self.line(speed=speed)


def demo():
    c = FakeCar()
    s = server.WebServer(c)

    try:
        s.run()
    except KeyboardInterrupt:
        c.stop_controller_ir()
        c.stop_controller_st()
        s.shutdown()
