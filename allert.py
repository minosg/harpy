#!/usr/bin/env python

"""allert.py: OS independant Allert handling ..."""

__author__ = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__   = "Minos Galanakis"
__project__ = "harpy"
__date__    = "01-10-2015"

import os
import sys
import platform
from subprocess import call, PIPE, Popen

# PiBlinker is not critical but should be imported if it exists
try:
    from piblinker import PiBlinker
except:
    pass


class AllertManager():

    def __init__(self):
        self.led_mode = False
        self.cmd = self.detectOS()

    def detectOS(self):
        """ Detect the running OS and set the notification cmd """
        systm = platform.system()

        # Detect Linux
        if systm == "Linux":
            if "Ubuntu" in platform.linux_distribution():
                cmd = "notify-send \"%s\""
            # Detect Raspberry Pi
            elif "armv7l" in platform.uname()[4]:
                try:
                    self.pb = PiBlinker()
                    self.led_mode = True
                except NameError:
                    print "Piblinker not found falling back to wall"
                except ImportError:
                    print "Piblinker shield missing falling back to wall"
                cmd = "wall \"%s\""
            else:
                cmd = "wall \"%s\""
        # Detect Windows
        elif systm == "win32":
            cmd = "cscript winallert.vbs \"%s\""
        # Requires gem install terminal notifier

        # Detect MacOS
        elif systm == "darwin":
            cmd = "terminal-notifier -message \"%s\""
        else:
            print "Did not detect known system, notifications disabled"
            raise ImportError
        return cmd

    def broadcast(self, message, color=None):
        """ Send the notification message and blink LED if color"""
        # If the sheild is attached use it as well
        if self.led_mode and color:
            try:
                pb.led_print(color, message)
                return
            except NameError:
                pass
        cmd = self.cmd % message
        ret, err = Popen(
            cmd, stdout=PIPE, stderr=PIPE, shell=True).communicate()

if __name__ == "__main__":
    am = AllertManager()
    am.broadcast("This is a test")
