from .irremote import Key
import threading
import time


class CarController:
    def __init__(self, car, handler, **kwargs):
        self.car = car
        self.handler = handler
        self.closed = False
        self.kwargs = kwargs
        self.thread = threading.Thread(target=self._run)

    def _run(self):
        self.handler(self, **self.kwargs)

    def run(self):
        self.thread.start()

    def shutdown(self):
        self.closed = True
        self.thread.join()


def infraredRemoteController(cc: CarController, speed=10):
    speed = min(99, max(0, speed))
    origin = speed
    while not cc.closed:
        key = cc.car.irremote.recieve()
        if key is Key.Num2:
            cc.car.fore(speed=speed)
        elif key is Key.Num8:
            cc.car.back(speed=speed)
        elif key is Key.Num5:
            cc.car.stop()
        elif key is Key.Num4:
            cc.car.left(speed=speed)
        elif key is Key.Num6:
            cc.car.right(speed=speed)
        elif key is Key.Minus:
            speed = max(0, speed - 10)
            cc.car.line(speed=speed)
        elif key is Key.Plus:
            speed = min(99, speed + 10)
            cc.car.line(speed=speed)
        elif key is Key.EQ:
            speed = origin
            cc.car.line(speed=speed)
        time.sleep(0.1)


def selfTraceController(cc: CarController, start=None, diff=500, speed=10, interval=0.1):
    if start is None or len(start) != 5:
        start = cc.car.irsensor.analog()
    while not cc.closed:
        current = cc.car.irsensor.analog()

        dis = 0
        for i in range(5):
            dis += abs(start[i] - current[i])

        if dis > diff:
            cc.car.left(speed)
            time.sleep(interval)
        else:
            cc.car.line(speed, 0)

        time.sleep(interval)


class Car:
    def __init__(self):
        from . import init
        from . import joystick
        from . import servo
        from . import led
        from . import irremote
        from . import irsensor
        from . import motor
        from . import distance

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
        self.controller_ir = None
        self.controller_st = None

    def start_controller_ir(self, speed=10):
        if self.controller_ir is not None:
            return
        self.controller_ir = CarController(
            self, infraredRemoteController, speed=speed)
        self.controller_ir.run()

    def stop_controller_ir(self):
        if self.controller_ir is None:
            return
        self.controller_ir.shutdown()
        self.controller_ir = None

    def start_controller_st(self, start=None, diff=500, speed=10, interval=0.1):
        if self.controller_st is not None:
            return
        self.controller_st = CarController(
            self, selfTraceController, start=start, diff=diff, speed=speed, interval=interval)
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
