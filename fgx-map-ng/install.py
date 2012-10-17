#!/usr/bin/env python

"""
The idea in the install script is to remove the pain of isntalling common stuff..

and instead contain in a managed enviroment, 
eg a shell script to install postigis, can be a django call from within the database

"""

import sys
import os
import commands
from optparse import OptionParser

from fgx.setup import INSTALLERS

## memcached BeautifulSoup4 python-yaml python-memcached (use djanjo from github)
# #manick if from head, 
# postgis is from tarballs


## Handle Command Args
usage = "usage: %prog [options] COMMAND\n"
usage += " commands:\n"
usage += "      chacks - Checks current install status\n"
usage += "      install [%s] - Install FGx package" % " | ".join(INSTALLERS)
parser = OptionParser(usage=usage)
parser.add_option(	"-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()

##########################################################
## Check we have a command
if len(args) == 0:
	parser.print_usage()
	sys.exit(0)

## Check its a valid comamnd
command = None
if args[0] in ['check', 'install', 'remove', 'status']:
	command = args[0]
else:
	parser.print_usage()
	sys.exit(0)
	
if command == "check":
	from fgx.setup import config
	
	print config.print_install_info()
	sys.exit(0)
	

## Validate install commands
if command == "install":
	if len(args) == 1:
		print "Error: Require and installer "
		parser.print_help()
		sys.exit(1)

	if not args[1] in INSTALLERS:
		print "Error: Installer `%s` not recognised " % args[1]
		parser.print_help()
		sys.exit(1)
	installer = args[1]

##===========================================
if command == "check":
	print check.check_installed(as_string=True)
	#print check.check_apt(as_string=True)
	
	
##########################################################################
if command == "install" and installer == "mapnik":
	
	print "Install Mapnik: >"
	
	setup.installer

