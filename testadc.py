#!/usr/bin/env python  
#
# print an adc value
# get_ain(chanum) where chanum 0 for CH0 on MCP3008 etc

import rpi_io
from time import sleep


while True:
    print rpi_io.get_ain(0)
    sleep(0.3)
