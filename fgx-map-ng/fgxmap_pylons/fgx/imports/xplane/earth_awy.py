
import sys
import fileinput
import datetime

from geoalchemy import WKTSpatialElement
from sqlalchemy.sql.expression import func 

from fgx.model import meta
from fgx.model.data import AirwaySegment, FGX_SRID
from fgx.lib import helpers as h



def import_dat( file_path, dev_mode=False, verbose=1, empty=False, clear=None):
	
	##file_path = UN_ZIP_DIR + "/earth_fix.dat"
	
	if verbose > 0:
		print "> Importing Fix: ", file_path
	
	started = datetime.datetime.now()
		
	meta.Sess.data.query(AirwaySegment).delete()
	meta.Sess.data.commit()
	

	
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
			
			#ident = parts[2]
			print parts
			
			

			## Create DB object
			ob = AirwaySegment()
			
			ob.ident_entry = parts[0]
			ob.ident_exit = parts[3]
			
			ob.level = int(parts[6])
			ob.fl_base = int(parts[7])
			ob.fl_top = int(parts[8])
			
			pnt =  'LINESTRING(%s %s, %s %s)' % (parts[1], parts[2], parts[4], parts[5])
			ob.wkb_geometry = func.ST_GeomFromText(pnt, FGX_SRID)
			
			#air_parts = parts[9].split("-")
			#print air_parts
			ob.airway = parts[9]
			
			meta.Sess.data.add(ob)			
			meta.Sess.data.commit()
			
		
		
		if dev_mode and c == 1000:
			sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	
	