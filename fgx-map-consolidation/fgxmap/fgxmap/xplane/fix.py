

import sys
import fileinput

from fgxmap.models import Fix

def import_dat(zx_path):
	
	
	print "yes", zx_path
	
	file_name = zx_path + "earth_fix.dat"
	print "FN=", file_name
	
	c = 0
	for raw_line in fileinput.input(file_name):
		c += 1
		line = raw_line.strip()
		print c, line
		
		fix = Fix()
		fix.ident = 
		
		if c == 10:
			sys.exit(0)