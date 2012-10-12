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
from fgx.mpnet import mp_telnet

##==============================================
## Dns
##==============================================
dnsLookupThread = dns_bot.DnsLookupThread()
dnsLookupThread.setDaemon(False)

def run():
	while True:
		
		if dnsLookupThread.is_alive():
			pass
		else:
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

