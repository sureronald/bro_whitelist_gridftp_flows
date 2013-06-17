# Triggered by Bro system call to notify web interface

import sys
import re
from optparse import OptionParser
import logging

__author__ = 'Ronald Osure (rosure@indiana.edu)'
__copyright__ = 'Copyright 2012, InCNTRE. This file is licensed under Apache 2.0'

LOGGING_PATH='/var/log/flow_notify.log'
LOGGING_LEVEL=logging.DEBUG

#Initialize logging basic config globally

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=LOGGING_PATH,level=LOGGING_LEVEL)

class FlowHandler:
    """
        Process flow connection data and notify web interface listener 
    """
    connection = None
    
    def __init__(self, connection):
        self.connection = connection
        logging.debug(self.connection)
        pass

def main():
    parser = OptionParser()
    parser.add_option("-c", "--connection", dest="connection", help="Bro connection object ie c$id")

    (options, args) = parser.parse_args()
    
    #logging.debug(options)
    #logging.debug(args)
     
    if options.connection is None:
        logging.fatal('Connection object empty! This should not happen')
        sys.exit(1)
    
    FlowHandler(options.connection)
    
if __name__ == '__main__':
    main()

