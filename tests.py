#Unit Tests

import os
import sys
import unittest

__author__ = 'Ronald Osure (rosure@indiana.edu)'
__copyright__ = 'Copyright 2012, InCNTRE. This file is licensed under Apache 2.0'

PATH = os.path.dirname(os.path.abspath(__file__))

if PATH not in sys.path:
    sys.path.append(PATH)

import flow_handler

class TestFlowHandler(unittest.TestCase):
    
    def test_host_port(self):
        self.assertEqual(('localhost', 1999,), flow_handler.HOST_PORT)
    
    def test_log_path(self):
        self.assertGreater(flow_handler.LOGGING_PATH, '', 'No log path given!')

if __name__=='__main__':
    unittest.main()
