#!/usr/bin/env python


## 
# This script does all the handling of the config
#
# @author Pete Morgan 
# @version 0.1.exp
# 

import sys
import os
from optparse import OptionParser

import fgx.app_global as G
from fgx.config import config

## Handle Command Args
usage = "usage: %prog [-h -j -n -s -v] "
parser = OptionParser(usage=usage)
parser.add_option(	"-j", 
					action="store_true", dest="js", default=False, 
					help="Write javascript configuration to `/etc/config.js`"
					)   
parser.add_option(	"-n", 
					action="store_true", dest="nginx", default=False, 
					help="Write nginx config to `/etc/nginx.conf`"
					) 
parser.add_option(	"-s", 
					action="store_true", dest="ln", default=False, 
					help="Write symlinks"
					) 
parser.add_option(	"-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )
parser.add_option(	"-l", 
					action="store_true", dest="local", default=False, 
					help="create local config file to `/local_config.yaml`"
					) 
(opts, args) = parser.parse_args()





#print opts, args
#print "js=", opts.js

#parser.print_usage()

if opts.local:
	print "Create local"
	
	dic = {"use_db": "n", "db": {"database": "aptdat850", "user": "fgx-map", "pass": "secret"}}
	
	dic['use_db'] = raw_input("Use database y/n (default: %s( ? " % dic['use_db'] ) or dic['use_db']
	
	if dic['use_db'] == "y":
		dic['db']['database'] = raw_input("Database Name (default: %s) ? " % dic['db']['database'] ) or dic['db']['database']
		dic['db']['user'] = raw_input("Database User (default: %s) ? " % dic['db']['user'] ) or dic['db']['user']
		dic['db']['pass'] = raw_input("Database password (default: %s) ? " % dic['db']['pass'] ) or dic['db']['pass']
	
	config.write_local_config({"config": dic})
	
	sys.exit(0)



if G.check_sane():
	print "errors"
	
	sys.exit(0)

if opts.js:

	config.write_js(ln=opts.ln)
	



