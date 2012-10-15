#!/usr/bin/env python
# turn on an LED when the switch is pressed
# put switch as shown in the lab diagram
# uses header P8
# GND     GND
# GPIO1_6 GPIO1_7
# GPIO1_2 (not used)
# switch uses port gpio2_7

import beagle_io
from time import sleep

try:
    while True:
        sw = beagle_io.get_din(71)
        if sw :
            beagle_io.on(38)
        else:
            beagle_io.off(38)

# this catches when you stop the program
except KeyboardInterrupt:
    beagle_io.off(38)
