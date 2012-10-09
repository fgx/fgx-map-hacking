#!/usr/bin/env python


import sys
import os
import commands
from optparse import OptionParser

import fgx.app_global as G
from fgx.installer import check


## Handle Command Args
usage = "usage: %prog [options] COMMANGS\n"
usage += " command: "
usage += "      check - Checks for packages isntalled etc"
parser = OptionParser(usage=usage)
parser.add_option(	"-v", nargs=1,
					action="store", type="int", dest="v", default=1,
					help="Prints more output 0-4 (0=none, 4=loads)"
                  )

(opts, args) = parser.parse_args()

if len(args) == 0:
	parser.print_usage()
	sys.exit(0)

#print opts, args


print check.check_apt()

