# Listener for new connection params (JSON formatted) from Bro & process

import logging
import SocketServer
import json

__author__ = 'Ronald Osure (rosure@indiana.edu)'
__copyright__ = 'Copyright 2012, InCNTRE. This file is licensed under Apache 2.0'

HOST_PORT = ('localhost', 2007,)

class BroConnectionTcpHandler(SocketServer.BaseRequestHandler):
    """
    TCP Handler Class
    """
    
    def _json_decode(self,data):
        try:
            json_data = json.loads(data)
        except ValueError,e:
            #logging.error("Failed to decode:"+data)
            return False
        return json_data
    
    def handle(self):
        while True:
            rec_tmp = self.request.recv(1024).strip()
            if not rec_tmp:
                break
            print rec_tmp
    
    def finish(self):
        pass

class SocketController:
    """
        Socket Controller
    """
    
    def __init__(self):
        pass
    
    def start_socket(self):
        #logging.debug("------------ Bro New Connection Listener Socket Started ------------")
        server = SocketServer.ThreadingTCPServer(HOST_PORT, BroConnectionTcpHandler)
        server.serve_forever()
    
    def shutdown_socket(self):
        server.shutdown()

if __name__ == '__main__':
    socket_controller = SocketController()
    socket_controller.start_socket()

