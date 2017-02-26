#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import requests
import subprocess
from time import sleep
import RPi.GPIO as GPIO

USER = ''
PASS = ''
MP3_PATH = './Ennio_Morricone.mp3'

STEPS_COUNT = 1000

class Door:
    # if STATE_FILE exists, the door is closed.
    state_file = './state_file'

    def is_open(self):
        return not self.is_closed()

    def is_closed(self):
        return os.path.exists(self.state_file)

    def open(self):
        os.remove(self.state_file)
        turn(STEPS_COUNT)
        requests.post('https://limugob.pythonanywhere.com/log', data={'message': 'DOOR_OPEN'}, auth=(USER,PASS))

    def close(self):
        self.pre_close_hook()
        file = open(self.state_file, 'w')
        file.close()
        turn(STEPS_COUNT, up=True)
        requests.post('https://limugob.pythonanywhere.com/log', data={'message': 'DOOR_CLOSE'}, auth=(USER,PASS))

    def pre_close_hook(self):
        # play some music before close
        print(subprocess.Popen(['mpg123', '-g 200', '-q', MP3_PATH]).wait())


# Verwendete Pins am Rapberry Pi
A=17
B=18
C=27
D=22

SLEEP_TIME = 0.001

def init():
    GPIO.setmode(GPIO.BCM)
    # Pins aus Ausaenge definieren
    GPIO.setup(A,GPIO.OUT)
    GPIO.setup(B,GPIO.OUT)
    GPIO.setup(C,GPIO.OUT)
    GPIO.setup(D,GPIO.OUT)
    GPIO.output(A, False)
    GPIO.output(B, False)
    GPIO.output(C, False)
    GPIO.output(D, False)

def Step1():
    GPIO.output(D, True)
    sleep (SLEEP_TIME)
    GPIO.output(D, False)

def Step2():
    GPIO.output(D, True)
    GPIO.output(C, True)
    sleep (SLEEP_TIME)
    GPIO.output(D, False)
    GPIO.output(C, False)

def Step3():
    GPIO.output(C, True)
    sleep (SLEEP_TIME)
    GPIO.output(C, False)

def Step3():
    GPIO.output(C, True)
    sleep (SLEEP_TIME)
    GPIO.output(C, False)

def Step4():
    GPIO.output(B, True)
    GPIO.output(C, True)
    sleep (SLEEP_TIME)
    GPIO.output(B, False)
    GPIO.output(C, False)

def Step5():
    GPIO.output(B, True)
    sleep (SLEEP_TIME)
    GPIO.output(B, False)

def Step6():
    GPIO.output(A, True)
    GPIO.output(B, True)
    sleep (SLEEP_TIME)
    GPIO.output(A, False)
    GPIO.output(B, False)

def Step7():
    GPIO.output(A, True)
    sleep (SLEEP_TIME)
    GPIO.output(A, False)

def Step8():
    GPIO.output(D, True)
    GPIO.output(A, True)
    sleep (SLEEP_TIME)
    GPIO.output(D, False)
    GPIO.output(A, False)


def turn(steps_count, up=False):
    steps = [Step1,
             Step2,
             Step3,
             Step4,
             Step5,
             Step6,
             Step7,
             Step8]

    if up:
        steps.reverse()

    try:
        init()
        for i in range(steps_count):
            for motor_step in steps:
                motor_step()

    finally:
        GPIO.cleanup()




