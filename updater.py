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

from allert import AllertManager

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
        self.am = AllertManager()
        super(PageUpdater, self).__init__()

    def get_table(self):
        return self.arp_table
    

    def add_to_table(self, ip, entry):
        """ Add a new entry to the ARP table and allert if it exists and is tracked """
        
        # If the device has the same IP as before
        if ip in self.arp_table.keys() and entry['mac'] == self.arp_table[ip]['mac']: print 1
        # If the ip has been modified but address still registered
        elif entry['mac'] in repr(self.arp_table):
          for key in self.arp_table:
            if self.arp_table[key]['mac'] == entry['mac']: 
               print 2
               break
            else: 
              print 3
              return False
        # If it does not exist add it to the table
        else:
          self.arp_table[ip] = entry
          print 4
          return True
        # Only broadcast allert if the device is tracked
        color = self.arp_table[ip]['color']
        if color:
          al = self.arp_table[ip]['alias']
          hst = self.arp_table[ip]['hostname']
          self.am.broadcast("%s AKA %s has joined the network"%(hst,al),color)
        return False

    def fake_refresh(self):

        #Pick a random device from the fake dataset and remove it
        idx = randint(0,len(data_d)-1)
        key = data_d.keys()[idx]
        # Add the new entry in the ARP table (this is will be replaced
        # by arp callbacks
        #self.arp_table[key] = data_d[key]
        #self.arp_table[key]["time"] = datetime.now()
        tempentry = data_d[key]
        tempentry["time"] = datetime.now()
        self.add_to_table(key,tempentry)

    def clear_color(self, color):
        for ipkey in self.arp_table.keys():
            entry = self.arp_table[ipkey]
            modified = False
            try:
                if entry['color'] == color: entry['color'] = ""
                modified = True
            except KeyError:
               pass
        return modified

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
