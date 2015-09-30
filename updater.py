#!/usr/bin/env python

"""updater.py: updater.py: Threaded class that updates the GUI
   with new data without user interaction ..."""

__author__  = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__   = "Minos Galanakis"
__project__ = "harpy"
__date__    = "30-09-2015"

from time import sleep
from threading import Thread, Event
from formatutils import *
from collections import OrderedDict
from random import randint
from copy import deepcopy
from datetime import datetime, timedelta

# TODO remove it when testing is complete
from test_dataset import data_d

thread_stop_event = Event()

class PageUpdater(Thread):
    def __init__(self, socketio_srv, poll_delay = 2):
        self.delay = poll_delay
        self.socketio = socketio_srv
        self.arp_table = {}
        super(PageUpdater, self).__init__()

    def fake_refresh(self):

        #Pick a random device from the fake dataset and remove it
        idx = randint(0,len(data_d)-1)
        key = data_d.keys()[idx]
        # Add the new entry in the ARP table (this is will be replaced
        # by arp callbacks
        self.arp_table[key] = data_d[key]

    def prune(self):
        """ Function that will remove old entries from arp_table"""
        pass

    def refresh(self):

        headers = ["IP","MAC","Hostname","Alias"]
        return tabularize_data(headers,self.arp_table)

    
    def run(self):
        while not thread_stop_event.isSet():
            self.fake_refresh()
            test_text = self.refresh()
            self.socketio.emit('newData', {'payload': test_text}, namespace='/autoreload')
            sleep(self.delay)

if __name__ == "__main__":
    pass