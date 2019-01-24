#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

AUTO_R = 4
AUTO_Y = 5
AUTO_G = 6

JALAN_R = 13
JALAN_G = 19

PAINIKE = 12
PAINIKE_LED = 26

TUNNISTIN = 20

GPIO.setmode(GPIO.BCM)

GPIO.setup(AUTO_R, GPIO.OUT, initial=0)
GPIO.setup(AUTO_Y, GPIO.OUT, initial=0)
GPIO.setup(AUTO_G, GPIO.OUT, initial=1)

GPIO.setup(JALAN_R, GPIO.OUT, initial=1)
GPIO.setup(JALAN_G, GPIO.OUT, initial=0)

GPIO.setup(PAINIKE_LED, GPIO.OUT, initial=0)
GPIO.setup(PAINIKE, GPIO.IN)
GPIO.setup(TUNNISTIN, GPIO.IN)

suojatiePyynto = False
suojatieKaytossa = False
edellinenPainallusAika = 0


def suojatiePainettu(channel):
    global suojatiePyynto
    global suojatieKaytossa
    global edellinenPainallusAika
    painallusVali = time.time() - edellinenPainallusAika
    edellinenPainallusAika = time.time()
    # lopettaa ohjelman tuplaklikkauksella
    if painallusVali < 0.4:
        print "Ohjelma lopetettu"
        GPIO.cleanup()
        raise SystemExit
    # asettaa suojatiepyynnon
    elif not suojatieKaytossa:
        print "Suojatiepyyntö vastaanotettu "
        suojatiePyynto = True
        GPIO.output(PAINIKE_LED, 1)

def tunnistus(channel):
    tila = GPIO.input(TUNNISTIN)
    #GPIO.output(PAINIKE_LED, tila)
    if tila:
        print "Tunnistaa liikettä"
    else:
        print "Ei tunnista liikettä"


GPIO.add_event_detect(PAINIKE, GPIO.RISING, callback=suojatiePainettu, bouncetime=100)

GPIO.add_event_detect(TUNNISTIN, GPIO.BOTH, callback=tunnistus, bouncetime=100)

def valosekvenssi():
    global suojatiePyynto
    global suojatieKaytossa
    # odota että liiketunnistin ei havaitse liikettä tai maksimi aika kulunut
    loppuAika = time.time() + 10
    while (GPIO.input(TUNNISTIN) and time.time() < loppuAika):
        time.sleep(0.1)
    # autotien valot keltaisen kautta punaiseksi
    GPIO.output(AUTO_Y, 1)
    GPIO.output(AUTO_G, 0)
    time.sleep(2)
    GPIO.output(AUTO_R, 1)
    GPIO.output(AUTO_Y, 0)
    time.sleep(3)
    # jalankulkijan valot vihreaksi
    GPIO.output(JALAN_R, 0)
    GPIO.output(JALAN_G, 1)
    suojatiePyynto = False
    suojatieKaytossa = True
    GPIO.output(PAINIKE_LED, 0)
    # jalankulkijan vihreä valo vilkkuu pari kertaa ennen vaihtumista punaiseksi
    time.sleep(3)
    GPIO.output(JALAN_G, 0)
    time.sleep(0.5)
    GPIO.output(JALAN_G, 1)
    time.sleep(0.5)
    GPIO.output(JALAN_G, 0)
    time.sleep(0.5)
    GPIO.output(JALAN_G, 1)
    time.sleep(0.5)
    # jalankulkijan valot punaiseksi
    GPIO.output(JALAN_R, 1)
    GPIO.output(JALAN_G, 0)
    suojatieKaytossa = False
    time.sleep(3)
    # autotien valot keltaisen kautta vihreäksi
    GPIO.output(AUTO_Y, 1)
    time.sleep(2)
    GPIO.output(AUTO_R, 0)
    GPIO.output(AUTO_Y, 0)
    GPIO.output(AUTO_G, 1)
    # autotien valot vihreänä vähintään minimiajan
    time.sleep(5)


while True:
    if suojatiePyynto:
        valosekvenssi()
    time.sleep(0.1)

