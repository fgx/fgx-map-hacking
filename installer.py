#!/usr/bin/env python


import sys
import os
from optparse import OptionParser

import fgx.app_global as G
from fgx.config import config

## Handle Command Args
usage = "usage: %prog [options] command\n"
usage += " command = check"
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
parser.add_option(	"-t", 
					action="store_true", dest="tilecache", default=False, 
					help="Write tilecache"
					) 
parser.add_option(	"-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )
parser.add_option(	"--make-local", 
					action="store_true", dest="local", default=False, 
					help="create local config file to `/local_config.yaml`"
					) 
(opts, args) = parser.parse_args()

print opts, args

print G.APT_PACKAGES

print "Check APT-Packages"

APT_CHECK = "dpkg-query -W -f='${Status} ${Version}\n' "

for p in G.APT_PACKAGES:
	print "\nChecking: %s" % p
	os.system(APT_CHECK + p)