#!/usr/bin/env python3
import rpi_io
import os
LED = 13
PID = os.getpid()
os.sched_setaffinity(PID, {0})
try:
    while True:
        rpi_io.on(LED)
        rpi_io.off(LED)
except KeyboardInterrupt:
    rpi_io.off(LED)

