
import sys
import fileinput

from django.contrib.gis.geos import Point, GEOSGeometry

from fgx.fix.models import Fix
import settings

print "TEMP", settings.TEMP_DIR

def import_dat(zip_dir, test_mode=False):
	
	print "zip_dir=", zip_dir
	
	file_path = zip_dir + "/earth_fix.dat"
	
	
	## Nuke existing entries
	Fix.objects.all().delete()
	
	c = 0
	for raw_line in fileinput.input(file_path):
		
		c += 1
		
		if c <= 3:
			## Skip first three lines, redits etc
			pass
		else:
			
		
			line = raw_line.strip()
			#print c, line
			parts = line.split()
			
			print ">>", parts
			
			#print parts
			parts = line.split()
			#pnt = Point(parts[0], parts[1]) ## << fails cos its a String ? 
			pnt = GEOSGeometry( 'POINT(%s %s)' % (parts[0], parts[1]) ) ## << WOrks 
			
			nuFix = Fix()
			nuFix.fix = parts[2]
			nuFix.geom = pnt
			
			nuFix.save()
			
		
		
		if test_mode and c == 1000:
			sys.exit(0)