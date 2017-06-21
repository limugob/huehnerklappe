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

STEPS_COUNT = 4000

class BadState(Exception):
    """Exception raised when operation and state don't fit together
    """
    pass

class Door:
    # if STATE_FILE exists, the door is closed.
    state_file = './state_file'

    def is_open(self):
        return not self.is_closed()

    def is_closed(self):
        return os.path.exists(self.state_file)

    def open(self):
        if self.is_open():
            raise BadState()
        os.remove(self.state_file)
        turn(STEPS_COUNT)
        # requests.post('https://limugob.pythonanywhere.com/log', data={'message': 'DOOR_OPEN'}, auth=(USER,PASS))

    def close(self):
        if self.is_closed():
            raise BadState()
        self.pre_close_hook()
        file = open(self.state_file, 'w')
        file.close()
        turn(STEPS_COUNT, up=True)
        # requests.post('https://limugob.pythonanywhere.com/log', data={'message': 'DOOR_CLOSE'}, auth=(USER,PASS))

    def pre_close_hook(self):
        # play some music before close
        print(subprocess.Popen(['mpg123', '-g 200', '-q', MP3_PATH]).wait())


# Verwendete Pins am Rapberry Pi
motor1 = (17, 18, 27, 22)
motor2 = (23, 24, 25, 4)

SLEEP_TIME = 0.001

def init(motor):
    GPIO.setmode(GPIO.BCM)
    # Pins aus Ausgaenge definieren
    GPIO.setup(motor[0],GPIO.OUT)
    GPIO.setup(motor[1],GPIO.OUT)
    GPIO.setup(motor[2],GPIO.OUT)
    GPIO.setup(motor[3],GPIO.OUT)
    GPIO.output(motor[0], False)
    GPIO.output(motor[1], False)
    GPIO.output(motor[2], False)
    GPIO.output(motor[3], False)

def Step1(motor1, motor2):
    GPIO.output(motor1[3], True)
    GPIO.output(motor2[3], True)
    sleep (SLEEP_TIME)
    GPIO.output(motor1[3], False)
    GPIO.output(motor2[3], False)

def Step2(motor1, motor2):
    GPIO.output(motor1[3], True)
    GPIO.output(motor1[2], True)
    GPIO.output(motor2[3], True)
    GPIO.output(motor2[2], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[3], False)
    GPIO.output(motor1[2], False)
    GPIO.output(motor2[3], False)
    GPIO.output(motor2[2], False)

def Step3(motor1, motor2):
    GPIO.output(motor1[2], True)
    GPIO.output(motor2[2], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[2], False)
    GPIO.output(motor2[2], False)

def Step4(motor1, motor2):
    GPIO.output(motor1[1], True)
    GPIO.output(motor1[2], True)
    GPIO.output(motor2[1], True)
    GPIO.output(motor2[2], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[1], False)
    GPIO.output(motor1[2], False)
    GPIO.output(motor2[1], False)
    GPIO.output(motor2[2], False)

def Step5(motor1, motor2):
    GPIO.output(motor1[1], True)
    GPIO.output(motor2[1], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[1], False)
    GPIO.output(motor2[1], False)

def Step6(motor1, motor2):
    GPIO.output(motor1[0], True)
    GPIO.output(motor1[1], True)
    GPIO.output(motor2[0], True)
    GPIO.output(motor2[1], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[0], False)
    GPIO.output(motor1[1], False)
    GPIO.output(motor2[0], False)
    GPIO.output(motor2[1], False)

def Step7(motor1, motor2):
    GPIO.output(motor1[0], True)
    GPIO.output(motor2[0], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[0], False)
    GPIO.output(motor2[0], False)

def Step8(motor1, motor2):
    GPIO.output(motor1[3], True)
    GPIO.output(motor1[0], True)
    GPIO.output(motor2[3], True)
    GPIO.output(motor2[0], True)
    sleep(SLEEP_TIME)
    GPIO.output(motor1[3], False)
    GPIO.output(motor1[0], False)
    GPIO.output(motor2[3], False)
    GPIO.output(motor2[0], False)


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
        init(motor1)
        init(motor2)
        for i in range(steps_count):
            for motor_step in steps:
                motor_step(motor1, motor2)

    finally:
        GPIO.cleanup()




