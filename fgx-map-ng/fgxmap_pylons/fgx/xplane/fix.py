
import sys
import fileinput
import datetime

from geoalchemy import WKTSpatialElement


from fgx.model import meta, Fix
from fgx.lib import helpers as h



#import geos
from django.contrib.gis.geos import GEOSGeometry, Point

"""
from fgx.nav.models import Fix
import settings
"""

#print "TEMP", settings.TEMP_DIR
##UN_ZIP_DIR = h.G().temp_dir("/unzipped/xplane/")

def import_dat( file_path, dev_mode=False, verbose=1, empty=False):
	
	##file_path = UN_ZIP_DIR + "/earth_fix.dat"
	
	if verbose > 0:
		print "> Importing Fix: ", file_path
	
	started = datetime.datetime.now()
		
	## Nuke existing entries
	if empty:
		if verbose > 0:
			print "  > Emptied fix table"
		Fix.objects.all().delete()
	
	#conn = db.session.condnection()

	
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
			"""
			obs = meta.Session.query(Fix).filter_by(fix=ident).all()
			print ident, "fixOb=", obs
			if len(obs) == 0:
				ob = Fix()
				ob.fix = ident
				meta.Session.add(ob)
				meta.Session.commit()
			else:
				ob = obs[0]
			#sql = "insert into fix(fix, wkb_geometry)values( %s, %s)"
			##conn.execute("insert into fix(fix)values( '%s')" % ident)
			##db.session.commit()
			"""
			## Check if fix in in DB already
			obs = meta.Session.query(Fix).filter_by(fix=ident).all()
			if len(obs) == 0:
				## Not in DB so create and add
				ob = Fix()
				meta.Session.add(ob)
			else:
				## Found, so its the first one
				ob = obs[0]
			
			## Update the object and save
			pnt =  'POINT(%s %s)' % (parts[0], parts[1])
			#print pnt
			#print "##", parts
			#print pnt
			ob.fix = ident
			ob.lat = parts[0]
			ob.lon = parts[1]
			#ob.wkb_geometry = WKTSpatialElement(pnt, geometry_type='POINT') #, settings.FGX_SRID)
			#ob.wkb_geometry = GEOSGeometry(pnt)
			meta.Session.commit()
			
		
		
		if dev_mode and c == 1000:
			sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	
	