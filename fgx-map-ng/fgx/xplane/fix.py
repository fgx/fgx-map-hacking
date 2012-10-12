
import sys
import fileinput

from django.contrib.gis.geos import Point

from fgx.fgxmap.models import Fix


def import_dat(zip_dir):
	
	print "YES", zip_dir
	
	file_path = zip_dir + "/earth_fix.dat"
	
	c = 0
	for raw_line in fileinput.input(file_path):
		
		c += 1
		
		if c <= 3:
			## Skip first three lines, redits etc
			pass
		else:
			
		
			line = raw_line.strip()
			print c, line
			
			parts = line.split()
			print parts
			
			nuFix = Fix()
			nuFix.fix = parts[2]
			nuFix.geom = Point(-122, 37)
			
			nuFix.save()
			
		
		
		if c == 10:
			sys.exit(0)