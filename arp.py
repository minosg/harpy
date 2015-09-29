#!/usr/bin/env python

"""arp.py:Arp resolution routines ..."""

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

class ARPHandler():

  def __init__(self):
    self.net_table = {}
  
  def arp_monitor_callback(self,pkt):
    """ Convert the return of the arp monitor to dictionary entries """

    if ARP in pkt and pkt[ARP].op in (1,2):
      hwaddr = pkt.sprintf(r"%ARP.hwsrc%")
      ipsrc  = pkt.sprintf(r"%ARP.psrc%")
      host   = self.arp_resolve(ipsrc)
      self.net_table[ipsrc] = {'hostname':self.arp_resolve(ipsrc),'mac':hwaddr, 'alias':''}
      print ("%s %s %s"%(host,ipsrc,hwaddr))
  
  def arp_monitor(self):
    """ Threaded monito proccess """

    #Add background processes   
    def background_arp_poll():
      sniff(prn=self.arp_monitor_callback, filter="arp", store=0)

    #covert to a thread and start it
    thread = threading.Thread(target=background_arp_poll)
    thread.daemon = True
    thread.start() 

  def arp_scan(self):
    """ Scan the network using ARP requests for alive hosts """

    conf.verb = 0
    ans,unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst="192.168.0.1/24"),timeout = 2,iface = "eth0",inter=0.1)

    hosts = {}
    for snd,rcv in ans:
      hwaddr = rcv.sprintf(r"%Ether.src%")
      ipsrc= rcv.sprintf(r"%ARP.psrc%")
      hosts[ipsrc] = {'hostname':'','mac':hwaddr, 'alias':''}
      hosts[ipsrc]['hostname']=self.arp_resolve(ipsrc)
    return hosts
 
  def arp_resolve(self, ip_target):
    """ Resolve the hostname for given ip address """

    return gethostbyaddr(ip_target)[0]

if __name__ == "__main__":
    ah = ARPHandler()
    #print ah.arp_scan()
    ah.arp_monitor()
    try:
      while True: pass
    except KeyboardInterrupt:
      print ah.net_table
