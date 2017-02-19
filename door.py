#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import requests

USER = ''
PASS = ''

class Door:
    # if STATE_FILE exists, the door is closed.
    state_file = './state_file'

    def is_open(self):
        return not self.is_closed()

    def is_closed(self):
        return os.path.exists(self.state_file)

    def open(self):
        os.remove(self.state_file)
        requests.post('https://limugob.pythonanywhere.com/log', data={'message': 'DOOR_OPEN'}, auth=(USER,PASS))

    def close(self):
        file = open(self.state_file, 'w')
        file.close()
        requests.post('https://limugob.pythonanywhere.com/log', data={'message': 'DOOR_CLOSE'}, auth=(USER,PASS))