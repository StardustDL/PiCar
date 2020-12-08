
import neopixel

_LED_COUNT = 4
_LED_PIN = 18
_LED_FREQ_HZ = 800000
_LED_DMA = 10
_LED_BRIGHTNESS = 255
_LED_INVERT = False
_LED_CHANNEL = 0
_LED_STRIP = neopixel.ws.WS2812_STRIP


class Led:
    def __init__(self, manager, index):
        self.manager = manager
        self.index = index
        self.close()

    def close(self):
        self.color = (0, 0, 0, 0)

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if len(value) == 3:
            value = (*value, 0)
        self._color = value
        self.manager.apply(self.index, *self._color)


class LedManager:
    def __init__(self):
        self.strip = neopixel.Adafruit_NeoPixel(
            _LED_COUNT,
            _LED_PIN,
            _LED_FREQ_HZ,
            _LED_DMA,
            _LED_INVERT,
            _LED_BRIGHTNESS,
            _LED_CHANNEL)
        self.strip.begin()
        self.brightness = 128
        self.leds = tuple([Led(self, i) for i in range(4)])

    def apply(self, index, red, green, blue, white=0):
        if 0 <= index < 4:
            self.strip.setPixelColorRGB(index, red, green, blue, white)
            self.strip.show()
        else:
            raise Exception(
                f"Invalid LED index, should be 0-3, but got {index}")

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        value = min(255, max(0, value))
        self._brightness = value
        self.strip.setBrightness(self._brightness)
        self.strip.show()
