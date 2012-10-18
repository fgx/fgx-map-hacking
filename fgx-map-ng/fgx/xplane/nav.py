
import datetime
import fileinput

from django.contrib.gis.geos import Point, GEOSGeometry

from fgx.nav.models import Ndb
import settings


class NAV_ROW_CODE:
	ndb = 2
	vor = 3
	ils = 4
	ils2 = 5
	gs = 6
	om = 7
	mm = 8
	im = 9
	dme = 12
	dme2 = 13
	
def process_ndb(parts):
	#0  1           2                  3   4    5     6   7    8 
	#2  05.25041700 -003.95802800      0   294  50    0.0 PB   ABIDJAN FELIX HOUPHOUET BOIGNY NDB
	print "NDB, ", parts
	
	
	
	ob = Ndb.objects.filter():
		
		
		
	
	

def import_dat(zip_dir, dev_mode=False, verbose=1, empty=False):
	
	file_path = zip_dir + "/earth_nav.dat"
	
	if verbose > 0:
		print "> Importing NAV: ", zip_dir
	
	started = datetime.datetime.now()
		
	## Nuke existing entries
	if empty:
		if sssverbose > 0:
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
			
			
			if row_code == 2:
				## Process NDB
				self.process_ndb(parts)
				
				
			
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
	
	