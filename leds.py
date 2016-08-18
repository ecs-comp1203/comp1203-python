#!/usr/bin/env python
# flash LEDs in sequence
# uses header P8
# GND     GND
# GPIO1_6 GPIO1_7
# GPIO1_2 (not used)
# calculate the number by 32* n + m, so 1_2 is 32+2

import rpi_io
from time import sleep

RED = 13
BLUE = 19
GREEN = 26
ontime = 0.3

try:
    while True:
        rpi_io.on(RED)
        sleep(ontime)
        rpi_io.off(RED)
        rpi_io.on(BLUE)
        sleep(ontime)
        rpi_io.off(BLUE)
        rpi_io.on(GREEN)
        sleep(ontime)
        rpi_io.off(GREEN)

# this catches when you stop the program
except KeyboardInterrupt:
    rpi_io.off(RED)
    rpi_io.off(BLUE)
    rpi_io.off(GREEN)
