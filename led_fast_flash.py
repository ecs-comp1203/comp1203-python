#!/usr/bin/env python
import rpi_io
import os
LED = 13
try:
    while True:
        rpi_io.on(LED)
        rpi_io.off(LED)
except KeyboardInterrupt:
    rpi_io.off(LED)

