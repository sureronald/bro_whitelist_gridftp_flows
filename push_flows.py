#!/usr/bin/env python

#Read pickle file, process the connection data and push them as OpenFlow rules to FlowScale

import pickle
import logging

__author__ = 'Ronald Osure (rosure@indiana.edu)'
__copyright__ = 'Copyright 2012, InCNTRE. This file is licensed under Apache 2.0'

PICKLE_FILE = 'flows_cache.pickle'

#Logging Settings

LOGGING_PATH='/var/log/push_flows.log' #IMPORTANT: Ensure this file is writable
LOGGING_LEVEL=logging.DEBUG

#Initialize logging basic config globally

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=LOGGING_PATH,level=LOGGING_LEVEL)

class PushFlows:
    """
    Read pickle file that is updated by flow_handler every interval, process the data, build openflow rules
    and send this to FlowScale
    """
    
    flows_cache = None
    
    def __init__(self):
        try:
            with open(PICKLE_FILE, 'rb') as f:
                self.flows_cache = pickle.load(f)
        except IOError:
            logging.fatal('Unable to open pickle file, please ensure flow_handler.py is running & Bro is sending connection\
            data')
            
        self._build_openflow_rule()
    
    def _build_openflow_rule(self):
        logging.debug('Building rule!!')
        logging.debug(self.flows_cache)
        pass

def main():
    pf = PushFlows()

if __name__ == '__main__':
    main()
