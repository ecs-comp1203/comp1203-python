#!/usr/bin/env python
#
# try the PWM output mode
# Red = GPIO 13

import RPi.GPIO as GPIO
from time import sleep
PAUSETIME = 0.02
RED = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED, GPIO.OUT)

p = GPIO.PWM(RED, 1000)
p.start(50)
while 1:
	for x in range(10,70):
		p.ChangeDutyCycle(x)
		sleep(PAUSETIME)
	for x in range(10,70):
		p.ChangeDutyCycle(70-x)
		sleep(PAUSETIME)
