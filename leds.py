#!/usr/bin/env python
#
# flash LEDs in sequence
# Red = GPIO 13
# Orange/Blue = GPIO 19
# Green = GPIO 26 

import rpi_io
from time import sleep

RED = 13
ORANGE = 19
GREEN = 26
ontime = 0.3

try:
    while True:
        rpi_io.on(RED)
        sleep(ontime)
        rpi_io.off(RED)
        rpi_io.on(ORANGE)
        sleep(ontime)
        rpi_io.off(ORANGE)
        rpi_io.on(GREEN)
        sleep(ontime)
        rpi_io.off(GREEN)

# this catches when you stop the program
except KeyboardInterrupt:
    rpi_io.off(RED)
    rpi_io.off(ORANGE)
    rpi_io.off(GREEN)
