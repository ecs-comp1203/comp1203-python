#!/usr/bin/env python
import rpi_io
import os
from time import sleep
delay = 0.1
LED = 13
try:
    while True:
        rpi_io.on(LED)
        sleep(delay)
        rpi_io.off(LED)
        sleep(delay)
except KeyboardInterrupt:
    rpi_io.off(LED)
