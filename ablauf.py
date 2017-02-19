import ephem
import datetime
import time
import os

# if STATE_FILE exists, the door is closed.
STATE_FILE = './state_file'

hildesheim = ephem.Observer()
hildesheim.lat = '52:09:17.2'
hildesheim.lon = '9:57:28.7'
hildesheim.horizon = '-6'

def open_door():
    pass

def close_door():
    pass

def wait_and_close_door():
    print('wait_and_close_door')
    utcnow = datetime.datetime.utcnow()
    utc_setting = hildesheim.next_setting(ephem.Sun(), use_center=True).datetime()
    time_diff = utc_setting - utcnow

    print('now:', datetime.datetime.now())
    print('Länge des schlafes:', time_diff)

    time.sleep(time_diff.seconds)

    print('Klappe schließt', datetime.datetime.now())
    file = open(STATE_FILE, 'w')
    file.close()
    wait_and_open_door()

def wait_and_open_door():
    print('wait_and_open_door')
    utcnow = datetime.datetime.utcnow()
    utc_setting = hildesheim.next_rising(ephem.Sun(), use_center=True).datetime()
    time_diff = utc_setting - utcnow

    print('now:', datetime.datetime.now())
    print('Länge des schlafes:', time_diff)

    time.sleep(time_diff.seconds)

    print('Klappe öffnet', datetime.datetime.now())
    os.remove(STATE_FILE)
    wait_and_close_door()


if __name__ == '__main__':
    if os.path.exists(STATE_FILE):
        wait_and_open_door()
    else:
        wait_and_close_door()
