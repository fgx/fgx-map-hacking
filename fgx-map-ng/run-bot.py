#!/usr/bin/env python

"""
Starts stops the mp-net bots

"""

import sys
import os
import time
import commands
from optparse import OptionParser



## Handle Command Args
usage = "usage: %prog [-h -j -n -s -v] "
parser = OptionParser(usage=usage)
parser.add_option(	"-i", nargs=1, 
					action="store", type="int",  dest="interval", default=1, 
					help="Write javascript configuration to `/etc/config.js`"
					)   

(opts, args) = parser.parse_args()



from fgx import shell_config

#from fgx.mpnet import dns_bot
from fgx.mpnet import mp_telnet



##==============================================
## Dns
##==============================================

def run_bot():
	while True:
		
		mp_telnet.update_cache()
		#print "update", datetime.datetime.now()
		#lag, flights = mp_telnet.fetch_telnet("mpserver14.flightgear.org", False)
		#print lag, len(flights)
		
		time.sleep(opts.interval)
		

		
run_bot()

"""dns_bot.DnsLookupThread()
dnsLookupThread.setDaemon(False)
"""

"""
def run():
	dnsLookupThread = None
	while True:
		
		if dnsLookupThread == None:
			dnsLookupThread = dns_bot.DnsLookupThread()
			dnsLookupThread.setDaemon(False)
			print "Started DNS lookup thread"
			dnsLookupThread.start()

		time.sleep(5)
		#mp_telnet.ping_run()
		
		print "WAKEUP"
		#dnsLookupThread.stop()

"""
"""
if "--run" in sys.argv:
	run()
else:
	print "Start the bot use --run"
	
print "<< exit"

"""