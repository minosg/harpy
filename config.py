#!/usr/bin/env python

"""config.py: Module Description ..."""

__author__ = "minos197@gmail.com"
__license__ = "LGPL"
__version__ = "0.0.1"
__email__ = "Minos Galanakis"
__project__ = "harpy"
__date__ = "02-10-2015"

import os
import sys
import simplejson as json
from copy import deepcopy

class ConfigManager():

    def __init__(self, conf_file = "config.json"):
        self.config_f = os.path.realpath(conf_file)

    def load_config(self):
        try:
            with open(self.config_f,"r") as F:
                cdata = F.read()
                F.close()
                config = json.loads(cdata)

        except (IOError,json.scanner.JSONDecodeError):
            print "IO Error"
        return config

    def save_config(self,config):
        """ Save the app configuration to a file """

        with open(self.config_f,"w") as F:
            F.write(json.dumps(config))
        F.close()
        
    def cache_config(self,config):
        """ Copy a configuration object to memory """
        self.cache = deepcopy(config)
        
    def pop_cached_config(self,config):
        """ Retrieve a configuration object from memory """
        
        config = deepcopy(self.cache)
        del(self.cache)

if __name__ == "__main__":
    pass
