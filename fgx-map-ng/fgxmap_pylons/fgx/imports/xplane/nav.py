##
# @namespace nav
# @brief Imports Xplane earth_nav.dat
# @see: http://data.x-plane.com/file_specs/XP%20NAV810%20Spec.pdf
#

import os
import datetime
import fileinput

from geoalchemy import WKTSpatialElement
from sqlalchemy.sql.expression import func 

from fgx.lib import helpers as h
from fgx.model import meta, Ndb, Vor, FGX_SRID


#import helpers as h

## The row codes for reading earth_nav
class NAV_TYPE:
	
	# Non Directional beacon
	ndb = 2
	
	# VOR, 
	vor = 3
	ils = 4
	ils2 = 5
	gs = 6
	om = 7
	mm = 8
	im = 9
	dme = 12
	dme2 = 13

## Tables to give stats for	
#tables_to_list = ['vor','ndb','fix']	



############################################
def ndb_2_db(parts, verbose=1, empty=False):
	#   lat         lon             elv/ft  khz rng_nm n/a ID 8>>>>> desciprions 
	#0  1           2                  3   4    5     6   7    8 
	#2  05.25041700 -003.95802800      0   294  50    0.0 PB   ABIDJAN FELIX HOUPHOUET BOIGNY NDB
	#print "NDB, ", parts
	
	ident = parts[7]
	

	ob = Ndb()
	ob.ident = ident
	
	pnt = 'POINT(%s %s)' % (parts[1], parts[2])
	ob.wkb_geometry = func.ST_GeomFromText(pnt, FGX_SRID)	
	ob.name = " ".join(parts[8:])
	
	elev_ft =  h.to_int(parts[3])
	ob.elevation_ft = elev_ft if elev_ft > 0 else None
	ob.elevation_m = int( float(ob.elevation_ft) * 0.3048) if ob.elevation_ft else None
	
	r_nm = h.to_int(parts[4])
	ob.range_nm = r_nm if r_nm > 0 else None
	ob.range_m = h.to_int(ob.range_nm) * 1852 if ob.range_nm else None
	
	ob.freq_khz = parts[4]  # TODO now come we have 4 didgit freq ??
	
	meta.Session.add(ob)
	meta.Session.commit()

	
############################################
def vor_2_db(parts, verbose=1, empty=False):
	#   lat         lon             elv/ft  khz rng_nm n/a ID 8>>>>> desciprions 
	#0  1           2                  3   4    5     6   7    8 
	#2  05.25041700 -003.95802800      0   294  50    0.0 PB   ABIDJAN FELIX HOUPHOUET BOIGNY NDB
	#print "VOR, ", parts
	
	ident = parts[7]
	
	ob = Vor()
	ob.ident = ident
	ob.name = " ".join(parts[8:])
	
	pnt = 'POINT(%s %s)' % (parts[1], parts[2])
	ob.wkb_geometry = func.ST_GeomFromText(pnt, FGX_SRID)	
	
	elev_ft = h.to_int(parts[3])
	ob.elevation_ft = elev_ft if elev_ft > 0 else None
	ob.elevation_m = int( float(ob.elevation_ft) * 0.3048) if ob.elevation_ft else None
	
	r_nm = h.to_int(parts[4])
	ob.range_nm = r_nm if r_nm > 0 else None
	ob.range_m = h.to_int(ob.range_nm) * 1852 if ob.range_nm else None
	
	ob.freq_mhz = parts[4]
	
	meta.Session.add(ob)
	meta.Session.commit()
	

def import_dat(file_path, dev_mode=False, verbose=1, empty=False):
	

	#file_path = unzipped_dir + "/earth_nav.dat"
	
	if verbose > 0:
		print "> Importing NAV: ", file_path
	
	started = datetime.datetime.now()
		
	## Nuke existing entries
	if empty:
		if sssverbose > 0:
			print "  > Emptied fix table"
		Fix.objects.all().delete()
	
	c = 0
	for raw_line in fileinput.input(file_path):
		
		c += 1
		
		#if c <= 3:
		#	## Skip first three lines, redits etc
		#	pass
		#else:
			
		line = raw_line.strip()		
		parts = line.split()
		
		if verbose > 0 and c % 500 == 0:
			print "  > line: %s %s " % (c, line)
		if verbose > 1:
			print "  > line %s >>" % c, parts
		
		if len(line) == 0:
			pass
		else:
			row_code = h.to_int(parts[0])
			print "row_code=", row_code
			if row_code == 2:
				## Process NDB
				ndb_2_db(parts, empty=empty, verbose=verbose)
				
			elif row_code == 3:
				vor_2_db(parts, empty=empty, verbose=verbose)
			
	
	
	if dev_mode and c == 1000:
		sys.exit(0)
			
			
	print "  >> Done, imported %s lines " % c
	

		
	
	
	
	
######################################################################	
## This splits the nav types into their "row_code" parts
# the files are writtedn out to nav/ROW_CODE.dat eg 2.dat for ndb
def split_to_seperate_files(verbose=1):
						
	if not os.path.exists(SPLIT_DIR):
		os.mkdir(SPLIT_DIR)	
	
	
	out_files = {}
	line_count = {}
	
	if verbose > 0:
		print "> Spliting NAV: ", DAT_FILE
	
	started = datetime.datetime.now()
		
	
	c = 0
	for raw_line in fileinput.input(DAT_FILE):
		
		c += 1
		
		if c <= 3:
			## Skip first three lines, redits etc
			pass
		else:
			
			line = raw_line.strip()
			
			if verbose > 0 and c % 500 == 0:
				print "  > line: %s %s " % (c, line)
			if verbose > 1:
				print "  > line %s >>" % c, 
			
			
			row_code = line.split()[0]
			
			#print "row_code=", row_code
			
			if not row_code in out_files:
				fout_name = row_code_file_path(row_code)
				out_files[row_code] = open(fout_name, "w")
				line_count[row_code] = 0
				print "Created file: %s" % fout_name 
			out_files[row_code].write( line + "\n" )
			line_count[row_code] += 1
			
	h.write_json(SPLIT_DIR + "summary.json", line_count)	
	
	
	
#########################################################################
## Imports a split_file
"""
def import_split_file(row_code, verbose=1, empty=None, dev_mode=False):
	
	# TODO check it valid row_code
	file_path =  row_code_file_path(row_code)
	print "  > Reading: %s" % file_path
	c = 0
	for raw_line in fileinput.input(file_path):
		
		line = raw_line.strip()
		parts = line.split()
		
		if row_code == NAV_TYPE.ndb:
			ndb_2_db(parts, verbose=verbose, empty=empty)
			
		elif row_code == NAV_TYPE.vor:
			vor_2_db(parts, verbose=verbose, empty=empty)
			
		else:
			print "ROw-code: %s not andled" % row_code
			sys.exit(0)
		
"""		