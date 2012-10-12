#!/usr/bin/env python

"""
Starts stops the mp-net bots

"""

import sys
import os
import time
import commands
from optparse import OptionParser


#import fgx_shell_config as conf


from fgx import shell_config

from fgx.mpnet import dns_bot

##==============================================
## Dns
##==============================================
dnsLookupThread = dns_bot.DnsLookupThread()
dnsLookupThread.setDaemon(True)

def run():
	while True:
		
		dnsLookupThread.start()

		time.sleep(5)
		mp_telnet.ping_run()
		
		print "WAKEUP"
		#dnsLookupThread.stop()


if "--run" in sys.argv:
	run()
	
else:
	print "Start the bot use --run"
	
print "<< exit"

