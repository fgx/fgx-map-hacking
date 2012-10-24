
import sys
import fileinput
import datetime

from fgx import db

from geoalchemy import WKTSpatialElement
from fgx.navaids.models import Fix
#from django.contrib.gis.geos import Point, GEOSGeometry

"""
from fgx.nav.models import Fix
import settings
"""
import settings

#print "TEMP", settings.TEMP_DIR
UN_ZIP_DIR = settings.TEMP_DIR + "/unzipped/xplane/"

def import_dat( dev_mode=False, verbose=1, empty=False):
	
	file_path = UN_ZIP_DIR + "/earth_fix.dat"
	
	if verbose > 0:
		print "> Importing Fix: ", UN_ZIP_DIR
	
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
			
			## Check if fix in in DB already
			obs = db.session.query(Fix).filter_by(fix=ident).all()
			if len(obs) == 0:
				## Not in DB so create and add
				ob = Fix()
				db.session.add(ob)
			else:
				## Found, so its the first one
				ob = obs[0]
			
			## Update the object and save
			pnt =  'POINT(%s %s)' % (parts[0], parts[1])
			#print pnt
			ob.fix = ident
			ob.wkb_geometry = WKTSpatialElement(pnt, geometry_type='POINT') #, settings.FGX_SRID)
			db.session.commit()
			
		
		
		if dev_mode and c == 1000:
			sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	
	