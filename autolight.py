#!/usr/bin/env python
# turn on LED if it is dark
# use LDR with adc for input and a gpio to an LED
import RPi.GPIO as GPIO
import adc
from time import sleep

LED = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT)

# turn off the light if its dark
try:
	while True:
	    value = adc.get_ain(0)
	    if value < 800 :
	        GPIO.output(LED,GPIO.HIGH)
	    else :
	        GPIO.output(LED,GPIO.LOW)
	    sleep(0.3)

# this catches when you stop the program to turn off LEDs
except KeyboardInterrupt:
    GPIO.cleanup()
