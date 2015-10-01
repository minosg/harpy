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
from test_dataset import get_data

thread_stop_event = Event()
data_d = get_data()
class PageUpdater(Thread):
    def __init__(self, socketio_srv, poll_delay = 2, prune_period = 7):
        self.delay = poll_delay
        self.socketio = socketio_srv
        self.arp_table = {}
        self.prune_period = prune_period
        super(PageUpdater, self).__init__()

    def get_table(self):
      return self.arp_table
      
    def fake_refresh(self):

        #Pick a random device from the fake dataset and remove it
        idx = randint(0,len(data_d)-1)
        key = data_d.keys()[idx]
        # Add the new entry in the ARP table (this is will be replaced
        # by arp callbacks
        self.arp_table[key] = data_d[key]
        self.arp_table[key]["time"] = datetime.now()

    def prune(self):
        """ Function that will remove old entries from arp_table"""
        
        now = datetime.now()
        for key in  self.arp_table.keys():
          dlta = now - self.arp_table[key]['time']
          # If equal and larger remove it
          if dlta.days >= self.prune_period: self.arp_table.pop(key)

    def refresh(self):

        headers = ["IP","MAC","Hostname","Alias", "Last Seen", "Color"]
        return tabularize_data(headers,self.arp_table)


    def run(self):
        while not thread_stop_event.isSet():
            self.fake_refresh()
            test_text = self.refresh()
            self.socketio.emit('newData', {'payload': test_text}, namespace='/autoreload')
            sleep(self.delay)

if __name__ == "__main__":
    pass
