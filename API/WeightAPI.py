#! /usr/bin/python2

import time
import sys

EMULATE_HX711=False

referenceUnit = 1
offset_value = -1821

if not EMULATE_HX711:
    import RPi.GPIO as GPIO
    from hx711 import HX711
else:
    from emulated_hx711 import HX711

def cleanAndExit():
    print("Cleaning...")
    if not EMULATE_HX711:
        GPIO.cleanup()
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(offset_value)
hx.reset()
hx.tare()

def getWeight():
    try:
        val = max(0, int(hx.get_weight(5)))
        hx.power_down()
        hx.power_up()
        return val

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

if __name__ == '__main__':
    while True:
        print(getWeight())
        time.sleep(0.1)