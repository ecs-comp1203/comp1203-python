#!/usr/bin/env python
# turn on LED if it is dark
# use LDR with adc for input and a gpio to an LED
import beagle_io
from time import sleep

# turn on the light if its dark
while True:
    adc =  beagle_io.get_ain(1)
    if adc > 3000 :
        beagle_io.on(38)                                                 
    else :
        beagle_io.off(38)
    sleep(0.3)
