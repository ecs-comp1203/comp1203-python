#!/usr/bin/env python
# turn on LED if it is dark
# use LDR with adc for input and a gpio to an LED
import RPi.GPIO
import adc
from time import sleep

LED = 13

GPIO.setmode(GPIO.BCM)

# turn off the light if its dark
while True:
    adc = adc.get_ain(0)
    if adc < 800 :
        GPIO.output(LED,GPIO.HIGH)
    else :
        GPIO.output(LED,GPIO.GPIO.LOW)
    sleep(0.3)
