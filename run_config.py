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
usage = "usage: %prog [options]\n"
#usage += "    commands are\n"
#usage += "       config_js  - sets up js\n"
#usage += "       build proj1 proj2 - Build one or more projects\n"
#usage += "       buildall - Build all projects\n"
parser = OptionParser(usage=usage)
parser.add_option(	"-j", "--js", 
					action="store_false", dest="js", default=False, 
					help="Write javascript configuration to `/www_static/js/layers.js`"
					)   
parser.add_option(	"-n", "--nginx", 
					action="store_false", dest="js", default=False, 
					help="Write nginx config to `/etc/nginx.conf`"
					)  
parser.add_option(	"-v", "--verbose", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()


print opts, args



