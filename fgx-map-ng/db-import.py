#!/usr/bin/env python

## 
# This script does all apt-dat importng
#
# @author Pete Morgan 
# @version 0.1.exp
# 


import sys
import os
from optparse import OptionParser

from fgx import shell_config

Z = "/home/fgxl/fgx-map/_temp/downloads/AptNav201204XP1000"

## Handle Command Args
usage = "usage: %prog [options] command args"
usage += " commands: \n"
usage += "    import [fix|apt] eg ./%prog import fix apt vor\n"
parser = OptionParser(usage=usage)
 
parser.add_option("-d", 
					action="store_true", dest="dev_mode", default=False,
					help="Developer stops after 1000"
                  )
                  
parser.add_option("-e", 
					action="store_true", dest="empty", default=False,
					help="Empty the table first, then use inserts"
                  )
                  
parser.add_option("-v", nargs=1,
					action="store", type="int", dest="verbose", default=1,
					help="Prints more verbose output 0-4 (0=none, 4=loads)"
                  )
(opts, args) = parser.parse_args()
#print  opts, args


############################################################
## Check args
if len(args) == 0:
	
	print "Error: need a command"
	parser.print_help()
	sys.exit(1)
	
if not args[0] in ["import", "empty", "nuke", "create"]:
	print "Error: `%s` is invalid command " % args[0]
	parser.print_help()
	sys.exit(1)

command = args[0]


############################################################
#print "COMMAND=", command

if command == "import":
	
	# @todo: tables
	#if table == "fix":
	
	from fgx.xplane import fix
	fix.import_dat(zip_dir=Z, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
	
	
	
	