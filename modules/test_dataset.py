
#!/usr/bin/env python

"""test_dataset.py: Generate Random network devices data for testing  ..."""

__author__  = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__   = "Minos Galanakis"
__project__ = "harpy"
__date__    = "01-10-2015"

from copy import deepcopy
from random import randint
from collections import OrderedDict
from datetime import datetime

def random_mac(mode=":"):
    """Return a random mac address."""

    mac = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % tuple(
        [randint(0, 255) for n in range(6)])
    if mode != ":":
        return mac.replace(":", mode)
    return mac


def random_host_list():
    return ["BThomehub",
            "freenas",
            "owncloud",
            "Kodi",
            "Plex",
            "PS4-%s" % random_mac("-"),
            "ILOCZ%X" % randint(0, 16777215),
            "HP%X" % randint(0, 16777215),
            "Android-%s" % random_mac(""),
            "Unknown-%s" % random_mac("-")]


def random_ip_list(router_ip="192.168.0.1"):
    """Return a list of random ip addresses based on the input router ip."""

    # The router is assumed to be the first device in the range
    start_addr = int(router_ip.split(".")[-1])
    # The ip range is limitted to 255
    base_ip = router_ip[:router_ip.rfind(".") + 1]
    # Return first the router and then the random entries
    return [router_ip] + ["%s%d" %
                          (base_ip, randint(start_addr, 255)) for n in range(9)]


def get_data(router_ip="192.168.0.1"):
    """Get a fake collection of data for testing."""

    hosts = random_host_list()
    ip_list = random_ip_list(router_ip)

    random_dataset = {}
    for ip in ip_list:
        hostname = hosts.pop(0)
        random_dataset[ip] = OrderedDict([('mac', random_mac()),
                                          ('hostname', hostname),
                                          ('alias', ''),
                                          ('time',datetime.now()),
                                          ("color", "") ])

    return deepcopy(random_dataset)

if __name__ == "__main__":
    # Simple test program to display the data generated

    data = get_data()
    for key in data.keys():
        print "************* IP: %s ***************" % key
        for entry in data[key].keys():
            print " %s: %s" % (entry, data[key][entry])
        print "\n"
