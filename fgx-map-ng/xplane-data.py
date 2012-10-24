#!/usr/bin/env python
#
# (c) 2012, Pete Morgan, wales
# GPLv2 or later
#



import sys
import os
#import commands
from optparse import OptionParser

"""
xpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "flask_app"))  
if not xpath in sys.path:
	sys.path.insert(0, xpath)
"""
from www import shell
from www.fgx.xplane import server, nav


## Handle Command Args
usage = "usage: %prog [options] COMMAND args\n"
usage += " commands:\n"
usage += "      avail - List and down zips from data.xplane.org server\n"
#usage += "      statuc - View local data status\n"
usage += "      split - Split files into bits [nav]\n"

parser = OptionParser(usage=usage)
parser.add_option(	"-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )
parser.add_option(	"-t", "--temp", nargs=1,
					action="store", type="string", dest="temp", default="_temp/",
					help="Sets temp directory"
                  )
(opts, args) = parser.parse_args()


##====== Validate Args ==========##

## Got a command ?
if len(args) == 0:
	parser.print_help()
	sys.exit(0)

##  Valid command ?
if not args[0] in ['avail', 'split']:
	print "Error: Unkown command %s" % args[0]
	parser.print_help()
	sys.exit(0)
	
command = args[0]	

	
	
##=======================================
## Execute Commands
##=======================================
	
##== List Remote Files
if command == "avail":
	server.show_downloads()
	
elif command == "split":
	#if not args[1] in TODO
	# crash
	
	if args[1] == "nav":
		## Split nav files
		nav.split_to_seperate_files()
		
	
	
##== Download a file
#elif command in ["download", "down", "d"]:
	
	
	

