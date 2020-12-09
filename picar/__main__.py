from . import car
from . import server

import sys
import threading


def runWebServer(web):
    web.run()


def product():
    c = car.Car()
    s = server.WebServer(c)

    tweb = threading.Thread(target=runWebServer, args=(s,))
    tweb.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        c.stop_controller_ir()
        c.stop_controller_st()
        s.shutdown()
        tweb.join()


if __name__ == "__main__":
    if "--demo" in sys.argv:
        from . import demo
        demo.demo()
    else:
        product()
