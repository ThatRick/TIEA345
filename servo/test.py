#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep


GPIO.setmode(GPIO.BCM)

OUT_PIN = 16

GPIO.setup(OUT_PIN, GPIO.OUT)

GPIO.output(16, 1)

running = True
while running:
    c = unicode(raw_input(' CMD: ')).lower()
    if c == 'q':
        running = False
    elif c == 'a':
        GPIO.output(OUT_PIN, 1)
    elif c == 's':
        GPIO.output(OUT_PIN, 0)
    else:
        print("Command '" + str(cmd) + "' not recognized")

GPIO.cleanup()