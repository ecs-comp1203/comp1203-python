#!/usr/bin/env python  
# use thermistor+4k7ohm on adc, when warm light up red LED, else blue
# Adc(1) is pin AIN0 4 up from usb end of P8 ...
# threshold has to be chosen by experiment
import rpi_io
from time import sleep
RED = 13
BLUE = 19

try:
    while True:
        t =  rpi_io.get_ain(0)
        print t
        if t > 800 :
            rpi_io.off(RED)
            rpi_io.on(BLUE)
        else :
            rpi_io.off(BLUE)
            rpi_io.on(RED)                                                        
        sleep(0.3)

# this catches when you stop the program to turn off LEDs
except KeyboardInterrupt:
    rpi_io.off(RED)
    rpi_io.off(BLUE)

