#!/usr/bin/env python


import sys
import os
import commands
from optparse import OptionParser

import fgx.app_global as G
from fgx.installer import check


## Handle Command Args
usage = "usage: %prog [options] COMMAND\n"
usage += " commands:\n"
usage += "      check - Checks for packages istalled\n"
usage += "      install [postgres|postgis] - Install apt package"
parser = OptionParser(usage=usage)
parser.add_option(	"-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()

## Check we have a command
if len(args) == 0:
	parser.print_usage()
	sys.exit(0)

## Check its a valid comamnd
command = None
if args[0] in ['check', 'install', 'remove']:
	command = args[0]
else:
	parser.print_usage()
	sys.exit(0)
	

if command == "install":
	#if args[1] == 
	pass


##===========================================
if command == "check":
	print check.check_installed(as_string=True)
	#print check.check_apt(as_string=True)
	
	

