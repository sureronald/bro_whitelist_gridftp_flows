#!/usr/bin/env python

#Read pickle file, process the connection data and push them as OpenFlow rules to FlowScale

import os
import sys
import pickle
import urllib2
import logging

if os.path.dirname(os.path.abspath(__file__)) not in sys.path:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import flowscale_settings as _fs

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
    
    def push_rule(self):
        """CAUTION: This function is untested and is in anticipation of possible support for Openflow 1.3 in flowscale
        and also custom changes to FlowScale REST API"""
        
        request = urllib2.Request(fs.HOSTNAME)
        request.add_header('datapathId', fs.DATAPATH)
        
        """ $client->addHeader( 'datapathId', $l_datapath );
    # tracked locally in our db.  someday FlowScale may handle this internally
    $client->addHeader( 'groupId', $l_gid );
    $client->addHeader('action', $l_action);
    $client->addHeader( 'groupName', $l_tag );
    $client->addHeader( 'inputSwitch', $l_datapath );
    $client->addHeader( 'outputSwitch', $l_datapath );
    $client->addHeader( 'inputPorts', '17' );
    $client->addHeader( 'outputPorts', $l_outport );
    # group_type just set to '1'
    $client->addHeader( 'type', '1' );
    # set to '1' since we are just adding one flow.
    $client->addHeader( 'maximumFlowsAllowed', '1' );
    # the IP we want redirected
    $client->addHeader( 'values', $l_ip );
    # set to some value at 800 or higher
    $client->addHeader( 'priority', '800' );
    $client->addHeader('networkProtocol', 'ip' );
    $client->addHeader('transportDirection', 'dst' );"""
        

def main():
    pf = PushFlows()

if __name__ == '__main__':
    main()
