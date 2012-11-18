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

from shell_config import config

from fgx.model import meta, MpServer
from fgx.queries import database
from fgx.lib import app_globals
from fgx.lib import helpers as h



x_files = ['fix', 'nav', 'ndb', 'vor']

## Handle Command Args
usage = "usage: %prog [options] command args"
usage += " commands: \n"
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


	
## Drop All
if command == "dropall":
	
	db_utils.drop_all_tables()
	sys.exit(0)



## Drop tables
if command == "drop":
	
	if len(args) == 1:
		print "Error: Need a table to drop "
		sys.exit(1)
	
	for a in args[1:]:
		database.drop_table(a)
	sys.exit(0)

	
#############################################################################	
	
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
	
		from fgx.imports.xplane import fix
		file_path = config['temp_dir'] + "/unzipped/xplane/earth_fix.dat"
		database.empty_table("fix")
		fix.import_dat(file_path, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)

	#elif x_file == "nav":
	#	from fgx.imports.xplane import nav
	#	nav.import_dat(zip_dir=Z, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)

	
	elif x_file == "ndb":
		from fgx.imports.xplane import nav
		database.empty_table("ndb")
		file_path = config['temp_dir'] + "/unzipped/xplane/nav_split/2.dat"
		nav.import_dat(file_path, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
		
	elif x_file == "vor":
		from fgx.imports.xplane import nav
		database.empty_table("vor")
		file_path = config['temp_dir'] + "/unzipped/xplane/nav_split/3.dat"
		nav.import_dat(file_path, dev_mode=opts.dev_mode, empty=opts.empty, verbose=opts.verbose)
		
	
	
	else:
		print "Error: File `%s` unhandled" % x_file
		
		
	