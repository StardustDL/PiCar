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

class WebServer:
    def __init__(self, car, port=9090):
        self.car = car
        self.port = port
        self.server = None
        self.wwwroot = os.path.join(os.path.split(__file__)[0], "wwwroot")

    def _core(self, environ, start_response):
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
            start_response("200 OK", [("Content-Type", tp), ("Content-Length", str(len(body)))])
            return [body]
        else:
            start_response("404 Not Found", [("Content-Type", "text/plain")])
            return ["404 Not Found".encode("utf-8")]


    def _get(self, path):
        if path.startswith("/api/"):
            return sel._get_api(path.replace("/api/", ""))
        if path == "/":
            path = "/index.html"

        fp = os.path.join(self.wwwroot, path.lstrip("/"))
        if not os.path.exists(fp):
            return None

        with open(fp, "r") as f:
            text = "".join(f.readlines())
            if path.endswith(".html"):
                return _html(text)
            elif path.endswith(".css"):
                return _css(text)
            elif path.endswith(".js"):
                return _js(text)
            else:
                return _plain(text)

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

        state = {
            "led": led,
            "irsensor": irsensor,
            "motor": motor
        }

        return _json(state)

    def _post(self, path, input_stream, length):
        return None

    def run(self):
        self.server = make_server("0.0.0.0", self.port, self._core)
        self.server.serve_forever()

if __name__=="__main__":
    from . import car
    c = car.Car()
    s = WebServer(c)
    s.run()

