#!/usr/bin/env python  
# print an adc value
# getAdc(2) is pin...
import rpi_io
from time import sleep


while True:
    print rpi_io.get_ain(0)
    sleep(0.3)
