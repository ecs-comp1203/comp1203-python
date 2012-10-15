#!/usr/bin/env python  
# use thermistor+4k7ohm on adc, when warm light up red LED, else blue
# Adc(1) is pin AIN0 4 up from usb end of P8 ...
# threshold has to be chosen by experiment
import beagle_io
from time import sleep
RED = 38
BLUE = 34

try:
    while True:
        t =  beagle_io.get_ain(1)
        print t
        if t > 3100 :
            beagle_io.off(RED)
            beagle_io.on(BLUE)
        else :
            beagle_io.off(BLUE)
            beagle_io.on(RED)                                                        
        sleep(0.3)

# this catches when you stop the program to turn off LEDs
except KeyboardInterrupt:
    beagle_io.off(34)
    beagle_io.off(38)
    beagle_io.off(39)

