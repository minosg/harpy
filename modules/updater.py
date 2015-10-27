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
from datetime import datetime, timedelta

thread_stop_event = Event()


class PageUpdater(Thread):

    def __init__(self, socketio_srv, arp_table_retriever, poll_delay=2):
        self.delay = poll_delay
        self.socketio = socketio_srv
        self.fetch_table =  arp_table_retriever
        self.arp_table = self.fetch_table()
        self._stop = Event()
        super(PageUpdater, self).__init__()
        self.daemon = True

    def get_table(self):
        """ Expose the internal arp table """

        return self.arp_table

    def clear_color(self, color):
        """ Clear a every color refference from a table """

        for ipkey in self.arp_table.keys():
            entry = self.arp_table[ipkey]
            modified = False
            try:
                if entry['color'] == color:
                    entry['color'] = ""
                modified = True
            except KeyError:
                pass
        return modified

    def refresh(self):
        """ Rerender the table calling the external getter method """

        self.arp_table = self.fetch_table()

        headers = ["IP", "MAC", "Hostname", "Alias", "Last Seen", "Color"]
        return tabularize_data(headers, self.arp_table)

    def run(self):
        """ Main Loop, re-renders table and pushes to client with js"""

        while not self._stop.isSet():
            test_text = self.refresh()

            self.socketio.emit(
                'newData', {
                    'payload': test_text}, namespace='/autoreload')
            sleep(self.delay)

    def stop(self):
        """ Kill the thread """

        self._stop.set()


if __name__ == "__main__":
    pass
