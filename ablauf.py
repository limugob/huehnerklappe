#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ephem
from datetime import datetime
import time
import os
from pytz import timezone
import pytz
import requests

import logging
logging.basicConfig(filename='/home/pi/huehnerklappe/ablauf.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

from door import Door

TIMEZONE = timezone('Europe/Berlin')
UTC = pytz.UTC

hildesheim = ephem.Observer()
hildesheim.lat = '52:09:17.2'
hildesheim.lon = '9:57:28.7'
hildesheim.horizon = '-6'

MIN_OPEN = {'hour' : 5, 'minute': 30, 'second': 0, 'microsecond': 0}  # earliest possible opening in localtime
MAX_CLOSE = {'hour' : 20, 'minute': 0, 'second': 0, 'microsecond': 0}  # latest possible closing in localtime

door = Door()

def wait_and_close_door():
    logging.debug('wait_and_close_door')
    hildesheim.date = datetime.now(UTC)

    # datetime of next setting
    next_setting = UTC.localize(hildesheim.next_setting(ephem.Sun(), use_center=True).datetime())

    # datetime of last possible closing
    dd = next_setting.astimezone(TIMEZONE)
    dd = dd.replace(**MAX_CLOSE).astimezone(UTC)

    logging.debug('next_setting: %s', next_setting)
    logging.debug('last_possible_closing: %s', dd)

    next_closing = min(next_setting, dd)

    time_diff = next_closing - datetime.now(UTC)

    logging.debug('now: %s', datetime.now(UTC).astimezone(TIMEZONE))
    logging.debug('Laenge des Schlafes: %s', time_diff)
    time.sleep(time_diff.seconds)
    logging.debug('Klappe schliesst: %s', datetime.now(UTC).astimezone(TIMEZONE))
    door.close()

def wait_and_open_door():
    logging.debug('wait_and_open_door')
    hildesheim.date = datetime.now(UTC)

    # datetime of next rising
    next_rising = UTC.localize(hildesheim.next_rising(ephem.Sun(), use_center=True).datetime())

    # datetime of earliest possible opening
    dd = next_rising.astimezone(TIMEZONE)
    dd = dd.replace(**MIN_OPEN).astimezone(UTC)

    logging.debug('next_rising %s', next_rising)
    logging.debug('earliest_possible_opening: %s', dd)

    next_opening = max(next_rising, dd)

    time_diff = next_opening - datetime.now(UTC)

    logging.debug('now: %s', datetime.now(UTC).astimezone(TIMEZONE))
    logging.debug('Laenge des Schlafes: %s', time_diff)

    time.sleep(time_diff.seconds)

    logging.debug('Klappe oeffnet: %s', datetime.now(UTC).astimezone(TIMEZONE))
    door.open()


if __name__ == '__main__':
    while True:
        if door.is_open():
            wait_and_close_door()
        else:
            wait_and_open_door()

