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
usage = "usage: %prog [options]"
parser = OptionParser(usage=usage)
 
parser.add_option("-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()
#print  opts, args

command = "fix"
print "COMMAND=", command
if command == "fix":
	from fgx.xplane import fix
	fix.import_dat(zip_dir=Z)
	
	
	
	