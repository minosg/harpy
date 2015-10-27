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
from copy import deepcopy
from multiprocessing import Process,Event, Queue
from random import randint
from allert import AllertManager
from time import sleep
from datetime import datetime, timedelta

arp_thread_stop_event = Event()

# TODO remove it when testing is complete
from test_dataset import get_data
data_d = get_data()


class ARPHandler(Process):

    def __init__(self, poll_delay=2, prune_period=3600):
        self.delay = poll_delay
        self.arp_table = {}
        self.prune_period = prune_period
        self.am = AllertManager()
        self._stop = Event()
        self.mute = False
        self.fake = False
        self.rxq = Queue(1)
        self.txq = Queue(1)
        super(ARPHandler, self).__init__()
        self.daemon = True

    def get_table(self):
        """Expose arp table by refference."""

        if not self.txq.empty():
            self.arp_table = self.txq.get()
        print "ARP Retrieve",self.arp_table.keys()

        return self.arp_table

    def update_table(self,table):
        """ Allow the client application to update the proccess ARP table """

        if self.rxq.emtpy:
            # Copy the table to class memory
            self.arp_table = deepcopy(table)
            # Copy the table to forked proccess memory
            self.rxq.put(table)
            return True
        else:
            return False

    def arp_monitor_callback(self, pkt):
        """Convert the return of the arp monitor to dictionary entries."""

        if ARP in pkt and pkt[ARP].op in (1, 2):
            hwaddr = pkt.sprintf(r"%ARP.hwsrc%")
            ipsrc = pkt.sprintf(r"%ARP.psrc%")
            host = self.arp_resolve(ipsrc)
            entry = OrderedDict(
                [('mac', hwaddr),
                 ('hostname', self.arp_resolve(ipsrc)),
                 ('alias', ''), ("time", datetime.now()),
                 ("color", "")])

            time.sleep(0.1)
            self.add_to_table(ipsrc, entry)

            print ("%s %s %s" % (host, ipsrc, hwaddr)), self.txq.empty()


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

        try: host = gethostbyaddr(ip_target)[0]
        except: host = "N.A"
        return host

    def prune(self):
        """Function that will remove old entries from arp_table."""

        # Copy the latest version of the table
        if self.txq.empty(): return False
        temp_table = self.txq.get()

        now = datetime.now()
        for key in temp_table.keys():
            dlta = now - temp_table[key]['time']
            # If equal and larger remove it
            if dlta.days >= self.prune_period:
                temp_table.pop(key)
        return self.update_table(temp_table)

    def add_to_table(self, ip, entry):
        """Add a new entry to the ARP table and allert if it exists and 
        is tracked."""

        #print "\nEntry", entry, len(self.arp_table), hex(id(self.arp_table)),self.arp_table.keys()
        # if there is a new table from application copy it to memory
        if not self.rxq.empty():
            print "Rx-sync"
            self.arp_table = self.rxq.get()

        # If there is space in the queue push the table from memory
        if self.txq.empty():  self.txq.put(self.arp_table)

        # If the device has the same IP as before
        if ip in self.arp_table.keys() and entry[
                'mac'] == self.arp_table[ip]['mac']: pass
        # If the ip has been modified but address still registered
        elif entry['mac'] in repr(self.arp_table):
            for key in self.arp_table:
                if self.arp_table[key]['mac'] == entry['mac']:
                    break
                else: return False
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
        """ Simulate ARP scan with preset fake data """

        # Pick a random device from the fake dataset and remove it
        idx = randint(0, len(data_d) - 1)
        #Sleep a random number of seconds 
        sleep(randint(0, 10))
        key = data_d.keys()[idx]
        # Add the new entry in the ARP table (this is will be replaced
        # by arp callbacks
        tempentry = data_d[key]
        tempentry["time"] = datetime.now()
        self.add_to_table(key, tempentry)

    def run(self):
        """ Main Thread Loop """
    
        # Both entries are blocking so no loop required
        try:
            if self.fake: 
                self.fake_sniff()
            else:
                sniff(prn=self.arp_monitor_callback, filter="arp", store=0)
        except KeyboardInterrupt:
            print "Proccess Exit"#, self.arp_table

    def fake_sniff(self):
        """ Blocking method to simulate sniffing with fake data """
        while True: self.fake_data()

    def set_fake(self):
        """ Set fakedata mode """
        self.fake = True

    def set_mute(self, mute=True):
        """ Disable Thread Reporting """

        self.mute = mute


if __name__ == "__main__":
    ah = ARPHandler()
    ah.start()
    try:
        while True:
            pass
    except KeyboardInterrupt: 
        print ah.arp_table
