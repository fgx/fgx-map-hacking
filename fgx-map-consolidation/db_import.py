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

from django_app import shell_config


print "TODODO"

This will setup the database, check etc

## Handle Command Args
usage = "usage: %prog [options] data ./path"
parser = OptionParser(usage=usage)
 
parser.add_option("-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()

if len(args) == 0:
	
	print "ERROR Not enught"
	parser.print_help()
	sys.exit(0)
	
	
command = args[0]



####################################


if command == "create":
	
	print "Create"

	sys.exit(0)


zx_path = "/home/fgxl/xplane-tools/_temp/AptNav201208XP1000/"


if command == "fix":
	
		from xplane import fix
		fix.import_dat(zx_path)
	
	
	
	