#!/usr/bin/env python3
import rpi_io
import os
from time import sleep
PID = os.getpid()
os.sched_setaffinity(PID, {0})
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
