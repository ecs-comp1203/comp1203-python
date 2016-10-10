#!/usr/bin/env python
#
# turn on an LED when the switch is pressed
# put switch as shown in the lab diagram
# 
# Swithc = GPIO 21
# LED = GPIO 13

import rpi_io
from time import sleep
SWITCH = 21
LED = 13
rpi_io.set_input(SWITCH)
try:
    while True:
        sw = rpi_io.get_din(SWITCH)
        if sw :
            rpi_io.on(LED)
        else:
            rpi_io.off(LED)

# this catches when you stop the program
except KeyboardInterrupt:
    rpi_io.off(LED)
