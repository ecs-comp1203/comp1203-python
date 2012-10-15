#!/usr/bin/env python
# flash LEDs in sequence
# uses header P8
# GND     GND
# GPIO1_6 GPIO1_7
# GPIO1_2 (not used)
# calculate the number by 32* n + m, so 1_2 is 32+2

import beagle_io
from time import sleep

RED = 38
GREEN = 39
BLUE = 34
ontime = 0.3
try:
    while True:
        beagle_io.on(RED)
        sleep(ontime)
        beagle_io.off(RED)
        beagle_io.on(GREEN)
        sleep(ontime)
        beagle_io.off(GREEN)
        beagle_io.on(BLUE)
        sleep(ontime)
        beagle_io.off(BLUE)

# this catches when you stop the program
except KeyboardInterrupt:
    beagle_io.off(34)
    beagle_io.off(38)
    beagle_io.off(39)
