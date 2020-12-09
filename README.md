# PiCar

An embedded application for toy-car controlling based on Raspberry Pi 3 Model B and AlphaBot2-Pi.

![](https://repository-images.githubusercontent.com/311939116/ae20aa80-3a16-11eb-921e-5ea0231f505d)

> This is the source codes of my programming assignment of the course Embedded Applications on Intelligent Systems (2020 Fall) at NJU.

## Features

- Motor
  - Going foreward or backward
  - Turning left or right
- Infrared remote control
- Self tracing
- Real-time camera
- Monitor and control by web
  - Interactive
  - Programmable

## Usage

```sh
python3 -m picar
```

There is a demo which uses a fake car implement. It is fully Python codes, so it doesn't need any embedded devices. Use the following commands to run it.

```sh
python3 -m picar --demo
```

Visit `http://localhost:19090` to control the toy car from browser.

The API of the website is at `http://localhost:19090/api/`.

## Dependencies

- [RPi.GPIO](https://github.com/yfang1644/RPi.GPIO) for accessing GPIO pins on Raspberry Pi.
- [rpi_ws281x](https://github.com/yfang1644/rpi_ws281x) for controlling LEDs on AlphaBot2.
- [Adafruit Python PureIO](https://github.com/yfang1644/Adafruit_Python_PureIO) for controlling servos on AlphaBot2.
  - [Adafruit Python GPIO](https://github.com/yfang1644/Adafruit_Python_GPIO)
  - [Adafruit Python PCA9685](https://github.com/yfang1644/Adafruit_Python_PCA9685)
- [wsgiref](https://docs.python.org/3/library/wsgiref.html) for web server.
- [Vue 3](https://github.com/vuejs/vue-next) for web client.
- [Ace](https://ace.c9.io/) for code editor in client.