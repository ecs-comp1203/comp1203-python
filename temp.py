#!/usr/bin/env python  
#
# use thermistor+8k2ohm on adc, when warm light up red LED, else green
# ain(0) is pin 1 of the MCP3008 ...
# threshold has to be chosen by experiment

import rpi_io
from time import sleep
RED = 13
ORANGE = 19
GREEN = 26

try:
    while True:
        t =  rpi_io.get_ain(0)
        print t
        if t > 800 :
            rpi_io.off(RED)
            rpi_io.on(GREEN)
        else :
            rpi_io.off(GREEN)
            rpi_io.on(RED)                                                        
        sleep(0.3)

# this catches when you stop the program to turn off LEDs
except KeyboardInterrupt:
    rpi_io.off(RED)
    rpi_io.off(GREEN)


