#Fire for each new connection

#Author: Ronald Osure (rosure@indiana.edu)
#Copyright 2012, InCNTRE. This file is licensed under Apache 2.0

global socket_host = "127.0.0.1";
global socket_port = "1999";

event new_connection(c: connection)
	{
		#Connect to socket for each new connection
		system(fmt("echo \"%s\" | nc -n -w1 %s %s", c$id, socket_host, socket_port));
	}
