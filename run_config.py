#!/usr/bin/env python


## 
# This script does all the handling of the config
#
# @author Pete Morgan 
# @version 0.1.exp
# 


import os

from optparse import OptionParser


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

(opts, args) = parser.parse_args()


print opts, args
#print "js=", opts.js

parser.print_usage()

if opts.js:
	#print "Write js"
	from fgx.config import config
	config.write_js(ln=opts.ln)
	



