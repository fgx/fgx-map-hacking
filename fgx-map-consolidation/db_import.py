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


## Handle Command Args
usage = "usage: %prog [options] data ./path"
parser = OptionParser(usage=usage)
 
parser.add_option("-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()
#print  opts, args

command = "fix"

if command == "fix":
	from fgx.xplane import fix

	
	
	
	