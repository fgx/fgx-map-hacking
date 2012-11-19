
import sys
import fileinput
import datetime

from geoalchemy import WKTSpatialElement
from sqlalchemy.sql.expression import func 

from fgx.model import meta, Fix, NavSearch, FGX_SRID
from fgx.lib import helpers as h


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
			
			if line == "99":
				print ">> Reached end of fix file"
				return
			
			parts = line.split()
			
			if verbose > 0 and c % 500 == 0:
				print "  > line: %s %s " % (c, line)
			if verbose > 1:
				print "  > line %s >>" % c, parts
			
			ident = parts[2]

			## Fix
			ob = Fix()
			
			ob.ident = ident
			ob.lat = parts[0]
			ob.lon = parts[1]
			
			pnt =  'POINT(%s %s)' % (parts[0], parts[1])
			ob.wkb_geometry = func.ST_GeomFromText(pnt, FGX_SRID)
			meta.Session.add(ob)
			
			## Search
			obs = NavSearch()
			obs.nav_type = "fix"
			obs.ident = ident
			obs.name = None
			obs.wkb_geometry = func.ST_GeomFromText(pnt, FGX_SRID)
			meta.Session.add(obs)
			
			meta.Session.commit()
			
		
		
		if dev_mode and c == 1000:
			sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	
	