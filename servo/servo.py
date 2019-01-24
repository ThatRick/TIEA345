#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
from time import sleep
from ServoController import Servo  


GPIO.setmode(GPIO.BCM)

PWM_PIN = 18
FREQ = 50

GPIO.setup(PWM_PIN, GPIO.OUT)
pwm = GPIO.PWM(PWM_PIN, FREQ)

servo = Servo(pwm, 2.4, 11.8)


running = True
while running:
    cmd = unicode(raw_input(' CMD: '))
    try:
        num = float(cmd)
        print('  Duty cycle: {} %'.format(num))
        servo.setpos(num)
    except ValueError:
        c = cmd.lower()
        if c == 'q':
            running = False
        elif c == 'a':
            servo.setpos(100)
        elif c == 's':
            servo.setpos(50)
        elif c == 'd':
            servo.setpos(0)
        elif c == 'e':
            servo.stop()        
        else:
            print("Command '" + str(cmd) + "' not recognized")

GPIO.cleanup()