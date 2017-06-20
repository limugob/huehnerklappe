#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import ephem
from datetime import datetime
import time
import os
from pytz import timezone
import pytz
import requests

from door import Door

TIMEZONE = timezone('Europe/Berlin')
UTC = pytz.UTC

hildesheim = ephem.Observer()
hildesheim.lat = '52:09:17.2'
hildesheim.lon = '9:57:28.7'
hildesheim.horizon = '-6'

MIN_OPEN = {'hour' : 8, 'minute': 0, 'second': 0, 'microsecond': 0}  # earliest possible opening in localtime
MAX_CLOSE = {'hour' : 20, 'minute': 0, 'second': 0, 'microsecond': 0}  # latest possible closing in localtime

door = Door()

def wait_and_close_door():
    print('wait_and_close_door')
    hildesheim.date = datetime.now(UTC)

    # datetime of next setting
    next_setting = UTC.localize(hildesheim.next_setting(ephem.Sun(), use_center=True).datetime())

    # datetime of last possible closing
    dd = next_setting.astimezone(TIMEZONE)
    dd = dd.replace(**MAX_CLOSE).astimezone(UTC)

    print('next_setting', next_setting)
    print('dd', dd)

    next_closing = min(next_setting, dd)

    time_diff = next_closing - datetime.now(UTC)

    print('now:', datetime.now(UTC).astimezone(TIMEZONE))
    print('Länge des Schlafes:', time_diff)
    time.sleep(time_diff.seconds)
    print('Klappe schließt', datetime.now(UTC).astimezone(TIMEZONE))
    door.close()

def wait_and_open_door():
    print('wait_and_open_door')
    hildesheim.date = datetime.now(UTC)

    # datetime of next rising
    next_rising = UTC.localize(hildesheim.next_rising(ephem.Sun(), use_center=True).datetime())

    # datetime of last possible opening
    dd = next_rising.astimezone(TIMEZONE)
    dd = dd.replace(**MIN_OPEN).astimezone(UTC)

    print('next_rising', next_rising)
    print('dd', dd)

    next_opening = max(next_rising, dd)

    time_diff = next_opening - datetime.now(UTC)

    print('now:', datetime.now(UTC).astimezone(TIMEZONE))
    print('Länge des Schlafes:', time_diff)

    time.sleep(time_diff.seconds)

    print('Klappe öffnet', datetime.now(UTC).astimezone(TIMEZONE))
    door.open()


if __name__ == '__main__':
    while True:
        if door.is_open():
            wait_and_close_door()
        else:
            wait_and_open_door()

