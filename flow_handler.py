#!/usr/bin/env python

# Triggered by Bro system call to notify web interface

import time
import sys
import re
import SocketServer
import logging
import pickle

__author__ = 'Ronald Osure (rosure@indiana.edu)'
__copyright__ = 'Copyright 2012, InCNTRE. This file is licensed under Apache 2.0'

#Socket Server Settigs

SERVER = None
HOST_PORT = ('localhost', 1999,)

#Flows data structure (note that the keys for access concatenates the orig_h and resp_h variables for quick access)
#We keep track of communicating ports just to reduce the number of rules we send to the switch
# FLOWS_CACHE = { 'orig_h-resp_h': {
#                                    'orig_p_range: [min, high],
#                                    'resp_p_range: [min, high],
#                                    'time': time.time() #Used for expiring values from the flows cache based on FLOW_CACHE_MAX_TIME
#                                   }
#               }

FLOWS_CACHE = {}

#Time it takes before a flow is dropped from the FLOWS_CACHE, default is 15 minutes (We can change this, the best value
#would be the average time it takes for gridftp traffic to complete transferring data)

FLOW_CACHE_MAX_TIME = 900 

#GridFTP Flow settings

GRIDFTP_CONTROL_PORT = 2811

#Logging Settings

LOGGING_PATH='/var/log/flow_handler.log' #IMPORTANT: Ensure this file is writable
LOGGING_LEVEL=logging.DEBUG

#Initialize logging basic config globally

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename=LOGGING_PATH,level=LOGGING_LEVEL)

class FlowTcpHandler(SocketServer.BaseRequestHandler):
    """
        Process flow connection data and notify web interface listener 
    """
    
    #Received flow connection data is read into this variable
    
    connection_str = ''
    
    #Pickle update file status
    
    flow_cache_update_pickle = False
    
    def handle(self):
        while True:
            data_recv = self.request.recv(1024).strip()
            if not data_recv:
                break
            self.connection_str += data_recv
        
        self.request.close()
        
        logging.debug(self.connection_str)
        
        if self.connection_str is '':
            logging.fatal('Connection object empty! This should not happen')
            
            #Should we execute a sys.exit and break? sys.exit(1)
            return
        
        #We now parse the connection string
        #Sample connection string obj: " [orig_h=149.159.4.26, orig_p=35030/tcp, resp_h=149.165.180.10, resp_p=80/tcp]"
        
        pattern = re.compile("([a-z_]+)=([A-Za-z0-9/\.:]+)")
        match_group = pattern.findall(self.connection_str)
        if len(match_group) < 4:
            logging.error("Error matching object, manual check recommeneded on: "+self.connection_str)
            return
        
        #Cast matching group tuples list to dict
        #Expected sample result after cast: {'orig_p': '35030/tcp', 'orig_h': '149.159.4.26', 'resp_p': '80/tcp', 'resp_h': '149.165.180.10'}
        
        conn_obj = dict(match_group)
        
        #We now strip the /tcp portion of the resp_p and orig_p and cast the values to int
        
        conn_obj['orig_p'] = conn_obj['orig_p'].replace('/tcp','')
        conn_obj['resp_p'] = conn_obj['resp_p'].replace('/tcp','')
        
        conn_obj['orig_p'] = int(conn_obj['orig_p'])
        conn_obj['resp_p'] = int(conn_obj['resp_p'])
        
        logging.debug(conn_obj)
        
        #We now add a flow to the data structure if it does not exist or update port range if needed
        #If communication is on port 2811 (control port), we put it where???XX$$$?????
        
        flow_key = conn_obj['orig_h'] + '-' + conn_obj['resp_h']
        
        if conn_obj['orig_p'] is GRIDFTP_CONTROL_PORT or conn_obj['resp_p'] is GRIDFTP_CONTROL_PORT:
            logging.debug('We have control port communication, how should I treat this?')
            logging.debug(con_obj)
        elif FLOWS_CACHE.has_key(flow_key):
            #We update the flow entry port range and the time too
            
            orig_ports = [conn_obj['orig_p']] + FLOWS_CACHE[ flow_key ]['orig_p_range'] #Join port values to one list
            resp_ports = [conn_obj['resp_p']] + FLOWS_CACHE[ flow_key ]['resp_p_range']
            
            FLOWS_CACHE[ flow_key ]['orig_p_range'] = [ min(orig_ports),
                                                       max(orig_ports)
                                                       ]
            FLOWS_CACHE[ flow_key ]['resp_p_range'] = [ min(resp_ports),
                                                       max(resp_ports)
                                                       ]
            FLOWS_CACHE[ flow_key ]['time'] = time.time()
            
            self.flow_cache_update_pickle = True
            
            logging.debug(FLOWS_CACHE[ flow_key ])
        else:
            #We create a new flow entry into the cache. Min and max port values are first assumed to be equal because
            #we only have one port for now and nothing to compare to
            
            FLOWS_CACHE[ flow_key ] = {
                                       'orig_p_range': [conn_obj['orig_p'], conn_obj['orig_p']],
                                       'resp_p_range': [conn_obj['resp_p'], conn_obj['resp_p']],
                                       'time': time.time()
                                       }
            
            self.flow_cache_update_pickle = True
        logging.debug(FLOWS_CACHE)
        
    
    def finish(self):
        """
        We need to dump the current status of the cache to a pickle file for reading by push_flows.py that processes the
        data and pushes them as rules to FlowScale.
        """
        if self.flow_cache_update_pickle:
            try:
                with open('flows_cache.pickle', 'wb') as f:
                    pickle.dump(FLOWS_CACHE,f)
            except IOError:
                logging.fatal("Unable to open flows_cache file for writing")
        
        self.flow_cache_update_pickle = False

class SocketController:
    """
        Socket Controller
    """
    
    def __init__(self):
        pass
    
    def start_socket(self):
        try:
            logging.debug("--------- New Connections Listener Started %s:%d ----------" % (HOST_PORT[0], HOST_PORT[1]))
            SERVER = SocketServer.ThreadingTCPServer(HOST_PORT, FlowTcpHandler)
            SERVER.serve_forever()
        except KeyboardInterrupt:
            logging.debug("--------- Caught Ctl ^C signal, socket shutting down ---------")
    
    def shutdown_socket(self):
        SERVER.shutdown()

def main():
    socket_controller = SocketController()
    socket_controller.start_socket()
    
    
if __name__ == '__main__':
    main()

