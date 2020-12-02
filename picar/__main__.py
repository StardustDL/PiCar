from . import car
from . import server

import threading

def runWebServer(web):
    web.run()

if __name__=="__main__":
    c = car.Car()
    s = server.WebServer(c)

    tweb = threading.Thread(target=runWebServer, args = (s,))
    tweb.start()

    c.runByRemote()

