#!/usr/bin/env python
# turn on LED if it is dark
# use LDR with adc for input and a gpio to an LED
import rpi_io
from time import sleep
LED = 13
# turn off the light if its dark
while True:
    adc =  rpi_io.get_ain(0)
    if adc > 800 :
        rpi_io.on(LED)                                                 
    else :
        rpi_io.off(LED)
    sleep(0.3)
