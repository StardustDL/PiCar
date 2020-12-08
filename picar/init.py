import RPi.GPIO as GPIO


def init():
    GPIO.setmode(GPIO.BCM)


def cleanup():
    GPIO.cleanup()
