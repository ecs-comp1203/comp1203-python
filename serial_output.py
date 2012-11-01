#!/usr/bin/env python
from sys import argv
from serial import Serial
from time import sleep

DEFAULT_STRING = "AAA"
PORT = "/dev/ttyO5"


try:
    if len(argv) == 2:
        # argument has been passed to the program
        outstr = argv[1]
    else:
        outstr = DEFAULT_STRING
    print "Outputing %s" % outstr
    SERIAL_PORT = Serial(PORT, 9600, timeout=0.1)
    while True:
        SERIAL_PORT.write(outstr)
        sleep(0.5)
except KeyboardInterrupt:
    SERIAL_PORT.close()
