#!/usr/bin/env python  
# print an adc value
# getAdc(2) is pin...
import beagle_io
from time import sleep


while True:
    print beagle_io.get_ain(1)
    sleep(0.3)
