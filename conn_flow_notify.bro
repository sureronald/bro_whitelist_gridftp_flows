#Fire for each new connection

#Author: Ronald Osure (rosure@indiana.edu)
#Copyright 2012, InCNTRE. This file is licensed under Apache 2.0

global python_path = "/usr/bin/python";
global flow_handler = "./flow_handler.py";

event new_connection(c: connection)
      {
	 #Call python script for each new connection
         system(fmt("%s %s -c \"%s\"", python_path, flow_handler, c$id));
      }


