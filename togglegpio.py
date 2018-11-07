#!/usr/bin/env python
# rapidly toggles a GPIO on/off
# arg: the pin number you want to toggle (13 19 26)
# Kirk Martinez 2018
from sys import argv
import RPi.GPIO as GPIO
import os

LED = 13

GPIO.setmode(GPIO.BCM)
if len(argv) == 2:
	LED = int(argv[1])
	GPIO.setup(LED, GPIO.OUT)
else:
	print "Arg: 13 19 or 26 for GPIO channel to toggle"
	exit()
try:
    while True:
        GPIO.output(LED,GPIO.HIGH)
        GPIO.output(LED,GPIO.LOW)

except KeyboardInterrupt:
        GPIO.output(LED,GPIO.LOW)

