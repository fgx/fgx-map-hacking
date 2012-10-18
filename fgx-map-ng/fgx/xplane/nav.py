
import datetime
import fileinput

from django.contrib.gis.geos import Point, GEOSGeometry

from fgx.nav.models import Ndb

import settings
import helpers as h

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
	
############################################
def process_ndb(parts, verbose=1, empty=False):
	#   lat         lon             elv/ft  khz rng_nm n/a ID 8>>>>> descipriont  
	#0  1           2                  3   4    5     6   7    8 
	#2  05.25041700 -003.95802800      0   294  50    0.0 PB   ABIDJAN FELIX HOUPHOUET BOIGNY NDB
	print "NDB, ", parts
	
	ident = parts[7]
	
	if empty:
		ob = Ndb()
	else:
		obs = Ndb.objects.filter(ident=ident)
		if len(obs) == 0:
			ob = Ndb()
		else:
			ob = obs[0]
		
	ob.wkb_geometry = GEOSGeometry( 'POINT(%s %s)' % (parts[1], parts[2]) )
	ob.ident = ident
	ob.name = " ".join(parts[8:])
	ob.elevation_ft = parts[3]
	ob.elevation_m = int( float(ob.elevation_ft) * 0.3048)
	ob.range_nm = parts[4]
	ob.range_m = h.to_int(ob.range_nm) * 1852
	ob.freq_khz = parts[4]
	
	ob.save()
	

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
			
			row_code = h.to_int(parts[0])
			print "row_code=", row_code
			if row_code == 2:
				## Process NDB
				process_ndb(parts, empty=empty, verbose=verbose)
				
				
			"""
			ident = parts[2]
			#pnt = Point(parts[0], parts[1]) ## << fails cos its a String ? 
			
			
			
			obs = Fix.objects.filter(fix=ident)
			if len(obs) == 0:
				ob = Fix()
			else:
				ob = obs[0]
			ob.fix = parts[2]
			ob.wkb_geometry = pnt
			ob.save()
			"""
		
		
		if dev_mode and c == 1000:
			sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	
	