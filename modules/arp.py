#!/usr/bin/env python

"""arp.py:Arp resolution controll module ..."""

__author__  = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__   = "Minos Galanakis"
__project__ = "codename"
__date__    = "28-09-2015"

import threading
from scapy.all import *
from socket import gethostbyaddr
from subprocess import call, PIPE, Popen
from collections import OrderedDict
from threading import Thread, Event
from random import randint
from allert import AllertManager
from time import sleep
from datetime import datetime, timedelta

arp_thread_stop_event = Event()

# TODO remove it when testing is complete
from test_dataset import get_data
data_d = get_data()


class ARPHandler(Thread):

    def __init__(self, poll_delay=2, prune_period=3600):
        self.delay = poll_delay
        self.arp_table = {}
        self.prune_period = prune_period
        self.am = AllertManager()
        self._stop = Event()
        self.mute = False
        super(ARPHandler, self).__init__()
        self.daemon = True

    def get_table(self):
        """Expose arp table by refference."""

        return self.arp_table

    def arp_monitor_callback(self, pkt):
        """Convert the return of the arp monitor to dictionary entries."""

        if ARP in pkt and pkt[ARP].op in (1, 2):
            hwaddr = pkt.sprintf(r"%ARP.hwsrc%")
            ipsrc = pkt.sprintf(r"%ARP.psrc%")
            host = self.arp_resolve(ipsrc)
            self.arp_table[ipsrc] = OrderedDict(
                [('mac', hwaddr),
                 ('hostname', self.arp_resolve(ipsrc)),
                 ('alias', ''), ("time", datetime.now()),
                 ("color", "")])
            print ("%s %s %s" % (host, ipsrc, hwaddr))

    def arp_monitor(self):
        """Threaded monitor proccess."""

        # Spawn yet another thread since sniff will block

        # Add background processes
        def background_arp_poll():
            sniff(prn=self.arp_monitor_callback, filter="arp", store=0)

        # covert to a thread and start it
        thread = threading.Thread(target=background_arp_poll)
        thread.daemon = True
        thread.start()

    def arp_scan(self):
        """Scan the network using ARP requests for alive hosts."""

        conf.verb = 0
        ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff') /
                         ARP(pdst="192.168.0.1/24"), timeout=2,\
                         iface="eth0", inter=0.1)

        hosts = {}
        for snd, rcv in ans:
            hwaddr = rcv.sprintf(r"%Ether.src%")
            ipsrc = rcv.sprintf(r"%ARP.psrc%")
            hosts[ipsrc] = {'hostname': '', 'mac': hwaddr, 'alias': ''}
            hosts[ipsrc]['hostname'] = self.arp_resolve(ipsrc)
        return hosts

    def arp_resolve(self, ip_target):
        """Resolve the hostname for given ip address."""

        return gethostbyaddr(ip_target)[0]

    def prune(self):
        """Function that will remove old entries from arp_table."""

        now = datetime.now()
        for key in self.arp_table.keys():
            dlta = now - self.arp_table[key]['time']
            # If equal and larger remove it
            if dlta.days >= self.prune_period:
                self.arp_table.pop(key)

    def add_to_table(self, ip, entry):
        """Add a new entry to the ARP table and allert if it exists and 
        is tracked."""

        # If the device has the same IP as before
        if ip in self.arp_table.keys() and entry[
                'mac'] == self.arp_table[ip]['mac']:
            pass
        # If the ip has been modified but address still registered
        elif entry['mac'] in repr(self.arp_table):
            for key in self.arp_table:
                if self.arp_table[key]['mac'] == entry['mac']:
                    break
                else:
                    return False
        # If it does not exist add it to the table
        else:
            self.arp_table[ip] = entry
            return True

        # If mute is asserted do not report
        if self.mute:
            return False

        # Only broadcast allert if the device is tracked
        try:
            color = self.arp_table[ip]['color']
        except KeyError:
            color = ''
        if color:
            al = self.arp_table[ip]['alias']
            hst = self.arp_table[ip]['hostname']
            self.am.broadcast(
                "%s AKA %s has joined the network" %
                (hst, al), color)
        return False

    def fake_data(self):
        # Pick a random device from the fake dataset and remove it
        idx = randint(0, len(data_d) - 1)
        key = data_d.keys()[idx]
        # Add the new entry in the ARP table (this is will be replaced
        # by arp callbacks
        tempentry = data_d[key]
        tempentry["time"] = datetime.now()
        self.add_to_table(key, tempentry)

    def run(self):
        """ Main Thread Loop """

        # Start the main monitor code    
        self.arp_monitor()
        while not self._stop.isSet():
            # Extra tasks can be performed here
            sleep(self.delay)

    def stop(self):
        """ Kill the thread """

        self._stop.set()

    def set_mute(self, mute=True):
        """ Disable Thread Reporting """

        self.mute = mute


if __name__ == "__main__":
    ah = ARPHandler()
    # print ah.arp_scan()
    ah.arp_monitor()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print ah.arp_table
