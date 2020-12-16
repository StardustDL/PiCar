from wsgiref.simple_server import make_server
import json
import os


def _json(obj):
    return "application/json", json.dumps(obj).encode("utf-8")


def _plain(text):
    return "text/plain", text.encode("utf-8")


def _html(text):
    return "text/html", text.encode("utf-8")


def _css(text):
    return "text/css", text.encode("utf-8")


def _js(text):
    return "application/javascript", text.encode("utf-8")

def _binary(bin: bytearray):
    return "", bytes(bin)

class WebServer:
    def __init__(self, car, port=19090):
        self.car = car
        self.port = port
        self.server = None
        self.wwwroot = os.path.join(os.path.split(__file__)[0], "wwwroot")
        self.host = "192.168.208.108"

    def _core(self, environ, start_response):
        host = environ.get("HTTP_HOST", "192.168.208.108:19090")
        self.host = host.split(":")[0]
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")
        contentLength = environ.get("CONTENT_LENGTH", "0")
        try:
            contentLength = int(contentLength)
        except:
            contentLength = 0

        response = None

        if method == "GET":
            response = self._get(path)
        elif method == "POST":
            inp = environ.get("wsgi.input", None)
            response = self._post(path, inp, contentLength)

        if response:
            tp, body = response
            start_response(
                "200 OK", [("Content-Type", tp), ("Content-Length", str(len(body)))])
            return [body]
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return ["404 Not Found".encode("utf-8")]

    def _get(self, path):
        if path.startswith("/api/"):
            return self._get_api(path.replace("/api/", ""))
        if path == "/":
            path = "/index.html"

        fp = os.path.join(self.wwwroot, path.lstrip("/"))
        if not os.path.exists(fp):
            return None

        if path.endswith(".html") or path.endswith(".css") or path.endswith(".js"):
            with open(fp, "r") as f:
                text = "".join(f.readlines())
                if path == "/index.html":
                    text = text.replace("192.168.208.108", self.host)
                if path.endswith(".html"):
                    return _html(text)
                elif path.endswith(".css"):
                    return _css(text)
                elif path.endswith(".js"):
                    return _js(text)
                else:
                    return _plain(text)
        else:
            buf = bytearray(os.path.getsize(fp))
            with open(fp, "rb") as f:
                f.readinto(buf)
            return _binary(buf)

        return None

    def _get_api(self, path):
        led = {
            "brightness": self.car.led.brightness,
            "leds": [l.color for l in self.car.led.leds]
        }
        irsensor = {
            "left": self.car.irsensor.left(),
            "right": self.car.irsensor.right(),
            "analog": self.car.irsensor.analog()
        }
        motor = {
            "A": {
                "direction": self.car.motorA.direction,
                "speed": self.car.motorA.speed
            },
            "B": {
                "direction": self.car.motorB.direction,
                "speed": self.car.motorB.speed
            }
        }
        controller = {
            "ir": self.car.controller_ir is not None,
            "st": self.car.controller_st is not None,
            "oa": self.car.controller_oa is not None,
        }

        state = {
            "led": led,
            "irsensor": irsensor,
            "motor": motor,
            "controller": controller
        }

        return _json(state)

    def _post(self, path, input_stream, length):
        try:
            body = input_stream.read(length)
            obj = json.loads(body)

            motor = obj.get("motor")
            if motor:
                motorA = motor.get("A")
                motorB = motor.get("B")
                if motorA:
                    self.car.motorA.direction = motorA["direction"]
                    self.car.motorA.speed = motorA["speed"]
                if motorB:
                    self.car.motorB.direction = motorB["direction"]
                    self.car.motorB.speed = motorB["speed"]

            led = obj.get("led")
            if led:
                self.car.led.brightness = led["brightness"]
                leds = led.get("leds")
                if leds:
                    for i, v in enumerate(leds):
                        if i > 3:
                            break
                        self.car.led.leds[i].color = tuple(v)

            controller = obj.get("controller")
            if controller:
                irup = controller.get("ir_up")
                if irup:
                    self.car.start_controller_ir(**irup)
                irdown = controller.get("ir_down")
                if irdown:
                    self.car.stop_controller_ir()

                stup = controller.get("st_up")
                if stup:
                    self.car.start_controller_st(**stup)
                stdown = controller.get("st_down")
                if stdown:
                    self.car.stop_controller_st()
                
                oaup = controller.get("oa_up")
                if oaup:
                    self.car.start_controller_oa(**oaup)
                oadown = controller.get("oa_down")
                if oadown:
                    self.car.stop_controller_oa()

            return _plain("Success")
        except:
            return _plain("Fail")

    def run(self):
        self.server = make_server("0.0.0.0", self.port, self._core)
        self.server.serve_forever(1)

    def shutdown(self):
        self.server.server_close()
