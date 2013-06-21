#Fire for each new connection

#Author: Ronald Osure (rosure@indiana.edu)
#Copyright 2012, InCNTRE. This file is licensed under Apache 2.0

global socket_host = "localhost";
global socket_port = "1999";

event new_connection(c: connection)
      {
	  	#Connect to socket for each new connection
         system(fmt("echo \"%s\" | nc %s %s", c$id, socket_host, socket_port));
      }
