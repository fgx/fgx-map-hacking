#!/usr/bin/env python


import sys
import os
from optparse import OptionParser

import fgx.app_global as G
from fgx.config import config


print G.APT_PACKAGES

print "Check APT-Packages"

APT_CHECK = "dpkg-query -W -f='${Status} ${Version}\n' "

for p in G.APT_PACKAGES:
	print "\nChecking: %s" % p
	os.system(APT_CHECK + p)