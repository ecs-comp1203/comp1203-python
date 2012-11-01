#!/usr/bin/env python
import beagle_io
from time import sleep
delay = 0.1
try:
    while True:
        beagle_io.on(38)
        sleep(delay)
        beagle_io.off(38)
        sleep(delay)
except KeyboardInterrupt:
    beagle_io.off(38)
