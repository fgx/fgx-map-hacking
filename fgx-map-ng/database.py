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

from www import shell
from www import settings
from www.fgx.dbase import db_utils



x_files = ['fix', 'nav', 'ndb', 'vor', 'apt', "all"]

## Handle Command Args
usage = "usage: %prog [options] command args"
usage += " commands: \n"
usage += "    create - create database scbemas\n"
usage += "    drop [tables] - eg drop fix ndb vor\n"
usage += "    dropall - Drops ALL database tables\n"
usage += "    import [fix|ndb|vor|nav|apt|all] eg ./%prog import fix apt vor\n"
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

## Check we have command
if len(args) == 0:
	
	print "Error: need a command"
	parser.print_help()
	sys.exit(1)
	
## Check command is valid
if not args[0] in ["import", "empty", "nuke", "create", "dropall", "drop"]:
	print "Error: `%s` is invalid command " % args[0]
	parser.print_help()
	sys.exit(1)
command = args[0]



#############################################################################

## Create
if command == "create":
	
	db_utils.create_all()
	sys.exit(0)


## Drop All
if command == "dropall":
	
	db_utils.drop_all()
	sys.exit(0)


## Check import command valid
if command == "import":
	if len(args) == 1:
		print "Error: Need a file: %s " % (" | ").join(x_files)
		sys.exit(1)
		
	if not args[1] in x_files:
		print "Error: Need a valid file: %s " % (" | ").join(x_files)
		sys.exit(1)
x_file = args[1]

############################################################
#print "COMMAND=", command


if command == "import":
	
	# @todo: tables
	if x_file == "fix":
	
		from fgx.xplane import fix
		fix.import_dat(dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
	
	elif x_file == "nav":
		from fgx.xplane import nav
		nav.import_dat(zip_dir=Z, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
	
	elif x_file == "ndb":
		from fgx.xplane import nav
		nav.import_split_file(nav.NAV_TYPE.ndb, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
		
	elif x_file == "vor":
		from fgx.xplane import nav
		nav.import_split_file(nav.NAV_TYPE.vor, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
		
	
	
	else:
		print "Error: File `%s` unhandled" % x_file
		
		
	