#!/usr/bin/env python

"""arp.py:Arp resolution routines ..."""

__author__  = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__   = "Minos Galanakis"
__project__ = "codename"
__date__    = "28-09-2015"

from scapy.all import *
import socket

class ARPHandler():

  def __init__(self):
    pass

  def arp_monitor_callback(self,pkt):
    if ARP in pkt and pkt[ARP].op in (1,2):
      return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

  def arp_monitor(self):
    sniff(prn=self.arp_monitor_callback, filter="arp", store=0)

  def arp_scan(self):
    conf.verb = 0
    ans,unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst="192.168.0.1/24"),timeout = 2,iface = "eth0",inter=0.1)

    hosts = {}
    for snd,rcv in ans:
      hwaddr = rcv.sprintf(r"%Ether.src%")
      ipsrc= rcv.sprintf(r"%ARP.psrc%")
      hosts[ipsrc] = {'hostname':'','mac':hwaddr}
      hosts[ipsrc]['hostname']=arp_resolve(ipsrc)
    return hosts
 
  def arp_resolve(ip_target):
    return socket.gethostbyaddr(ip_target)[0]

if __name__ == "__main__":
    pass
