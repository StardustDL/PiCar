from enum import Enum
import selectors

class Key(Enum):
    CHMinus = 0x45
    CH = 0x46
    CHPlus = 0x47
    Left = 0x44
    Right = 0x40
    Play = 0x43
    Minus = 0x07
    Plus = 0x15
    EQ = 0x09
    Num0 = 0x16
    Num100 = 0x19
    Num200 = 0x0d
    Num1 = 0x0c
    Num2 = 0x18
    Num3 = 0x5e
    Num4 = 0x08
    Num5 = 0x1c
    Num6 = 0x5a
    Num7 = 0x42
    Num8 = 0x52
    Num9 = 0x4a


class IRRemote:
    def __init__(self):
        self.input = open("/dev/input/event0", "rb")
        self.selector = selectors.DefaultSelector()
        self.selector.register(self.input, selectors.EVENT_READ)

    def __del__(self):
        self.input.close()

    def recieve(self):
        events = self.selector.select(1)
        if len(events) == 0:
            return None
        value = int(self.input.read(48).hex()[40:42], base=16)
        return Key(value)
