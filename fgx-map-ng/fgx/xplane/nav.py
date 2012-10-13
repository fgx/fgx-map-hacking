
from django.contrib.gis.geos import Point, GEOSGeometry

from fgx.nav.models import Fix
import settings

print "TEMP", settings.TEMP_DIR

def import_dat(zip_dir, dev_mode=False, verbose=1, empty=False):
	
	file_path = zip_dir + "/earth_fix.dat"
	
	if verbose > 0:
		print "> Importing Fix: ", zip_dir
	
	started = datetime.datetime.now()
		
	## Nuke existing entries
	if empty:
		if verbose > 0:
			print "  > Emptied fix table"
		Fix.objects.all().delete()
	
	c = 0
	for raw_line in fileinput.input(file_path):
		
		c += 1
		
		if c <= 3:
			## Skip first three lines, redits etc
			pass
		else:
			
			line = raw_line.strip()
			parts = line.split()
			
			if verbose > 0 and c % 500 == 0:
				print "  > line: %s %s " % (c, line)
			if verbose > 1:
				print "  > line %s >>" % c, parts
			
			ident = parts[2]
			#pnt = Point(parts[0], parts[1]) ## << fails cos its a String ? 
			pnt = GEOSGeometry( 'POINT(%s %s)' % (parts[0], parts[1]) ) ## << WOrks 
			
			
			obs = Fix.objects.filter(fix=ident)
			if len(obs) == 0:
				ob = Fix()
			else:
				ob = obs[0]
			ob.fix = parts[2]
			ob.wkb_geometry = pnt
			ob.save()
			
		
		
		if dev_mode and c == 1000:
			sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	
	