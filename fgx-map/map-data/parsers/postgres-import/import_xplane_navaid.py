#!/usr/bin/env python

#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#
# Better remove the bad design with the globals instead. Thanks.

import sys, time, datetime, csv, os, re, psycopg2, yaml, warnings

# geographiclib 1.24 by (c) Charles Karney
from geographiclib.geodesic import Geodesic

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python import_xplane_navaid.py <file.dat>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python import_xplane_navaid.py <file.dat>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]

starttime = time.asctime()

with open("import_xplane_navaid.log", "a") as log:
	log.write("Import started: "+starttime+"\n")
	log.close()

conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']
if "host" in confMap:
	connectstring += " host=%s" % confMap['host']
conn = psycopg2.connect(connectstring)
cur = conn.cursor()

readnav = open(inputfile)

entrycount = 0

def drawcircle(rangerad,lon,lat):
    # We need 0 and 360 to close the polygon, see closepoly
	# What's a 'cricle' ? Should be sufficient to draw arc with 36 points.
	azi_list = range(0,360,10)
	circlelist = "POLYGON(("
	for i in azi_list:
		# Now be aware of this, geographiclib has lat/lon ordering, and not lon/lat
		result = Geodesic.WGS84.Direct(float(lat),float(lon),i,float(rangerad))
		# get it back in the right order
		circlelist += str(result["lon2"])+" "+str(result["lat2"])+","
	
	# End point
	closepoly = Geodesic.WGS84.Direct(float(lat),float(lon),0,float(rangerad))
	endpoint = str(closepoly["lon2"])+" "+str(closepoly["lat2"])
	
	circlelist += endpoint+"))"
	return circlelist

def insert_navaid(nav_ident,\
				apt_ident,\
				rwy_ident,\
				nav_elev_ft,\
				nav_freq_khz,\
				nav_freq_mhz,\
				nav_bearing_true,\
				nav_var_deg,\
				nav_name,\
				nav_suffix,\
				nav_center_lon84,\
				nav_center_lat84,\
				nav_range_nm,\
				nav_bias_nm,\
				nav_standalone,\
				nav_no_freq,\
				nav_xplane_code):
				
	'''nav_ident,apt_ident,rwy_ident,nav_elev_ft,nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code'''
	'''separated: nav_center,nav_center_lon,nav_center_lat,nav_range_poly'''
	
	nav_center = "POINT("+nav_center_lon84+" "+nav_center_lat84+")"
	
	sql = '''INSERT INTO navaid (nav_ident,apt_ident,rwy_ident,nav_elev_ft,nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code,nav_center)
		VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	
	
	params = [nav_ident,apt_ident,rwy_ident,nav_elev_ft,nav_freq_khz,nav_freq_mhz,nav_bearing_true,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,nav_standalone,nav_no_freq,nav_xplane_code,nav_center]
	
	print "Inserted: "+nav_ident
	
	try:
		cur.execute(sql, params)
	except:
		print "Database Error, check sql and parameters."
		
	# query gives lon/lat (postgis x/y) as text for the center point in reprojected format
	sql2 = "UPDATE navaid SET nav_center_lon=ST_X(nav_center), nav_center_lat=ST_Y(nav_center) WHERE nav_ident='"+nav_ident+"';"
	cur.execute(sql2)
	
	conn.commit()



##############################################################################################################
# XPlane Nav 810 Data specs
##############################################################################################################
#  2 NDB (Non-Directional Beacon)                       Includes NDB component of Locator Outer Markers (LOM)
#  3 VOR (including VOR-DME and VORTACs)                Includes VORs, VOR-DMEs and VORTACs
#  4 Localiser component of an ILS
#  5 Localiser component of a localiser-only approach   Includes for LDAs and SDFs
#  6 Glideslope component of an ILS                     Frequency shown is paired frequency, not the DME channel
#  7 Outer markers (OM) for an ILS                      Includes outer maker component of LOMs
#  8 Middle markers (MM) for an ILS
#  9 Inner markers (IM) for an ILS

# 12 DME, including the DME component of an ILS,        Frequency display suppressed on X-Plane's charts
#    VORTAC or VOR-DME                                          

# 13 Stand-alone DME, or the DME component              Frequency will displayed on X-Plane's charts
#    of an NDB-DME        
##############################################################################################################

def fillthenav():

	marker_count = 1000

	for line in readnav:
	
		#print line
	
		spaceremoved = " ".join(line.split())
		list = spaceremoved.split(" ")
		listlen = len(list)
	
		nav_standalone = "0"
		nav_no_freq = "1"
		
		try:
			nav_xplane_code = str(list[0])
			nav_center_lat84 = str(list[1])
			nav_center_lon84 = str(list[2])
			nav_elev_ft = str(list[3])
	
			# NDB Non-directional beacon
			if line.startswith("2 "):
				nav_freq_khz = str(list[4])
				nav_range_nm = str(list[5])
				# [6] not used for NDB
				nav_ident = str(list[7])
				nav_name = str(list[8:listlen-1]).replace("', '", " ").replace("['","").replace("']","").replace("[]","")
				# specifier is not separated in xplane data, we need the last one
				nav_suffix = str(list[listlen-1])
				#insert_navaid(nav_ident, None, None, nav_elev_ft, nav_freq_khz, None, None, None, nav_name, nav_suffix, nav_center_lon84,nav_center_lat84, nav_range_nm, None, None, None, nav_xplane_code)
					
			# VOR, includes VOR-DMEs and VORTACs
			if line.startswith("3 "):
				nav_freq_mhz = str(list[4])
				nav_range_nm = str(list[5])
				nav_var_deg = str(list[6])
				nav_ident = str(list[7])
				nav_name = str(list[8:listlen-1]).replace("', '", " ").replace("['","").replace("']","").replace("[]","")
				# specifier is not separated in xplane data, we need the last one
				nav_suffix = str(list[listlen-1])
				#insert_navaid(nav_ident,None,None,nav_elev_ft,None,nav_freq_mhz,None,nav_var_deg,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,None, None, None, nav_xplane_code)
		
			# LOC, includes localisers (inc. LOC-only), LDAs and SDFs 
			if line.startswith("4 ") or line.startswith("5 "):
				nav_freq_mhz = str(list[4])
				nav_range_nm = str(list[5])
				nav_bearing_true = str(list[6])
				nav_ident = str(list[7])
				apt_ident = str(list[8])
				rwy_ident = str(list[9])
				nav_name = str(list[10:listlen]).replace("', '", " ").replace("['","").replace("']","").replace("[]","")
				# specifier is not separated in xplane data, we need the last one
				nav_suffix = str(list[listlen-1])
				if line.startswith("4 "):
					nav_standalone = "0"
				else:
					nav_standalone = "1"
				#insert_navaid(nav_ident,apt_ident,rwy_ident,nav_elev_ft,None,nav_freq_mhz,nav_bearing_true,None,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,None,nav_standalone,None,nav_xplane_code)
				
			# GS, Glideslope associated with an ILS 
			if line.startswith("6 "):
				nav_freq_mhz = str(list[4])
				nav_range_nm = str(list[5])
				# Glideslope angle multiplied by 100,000 and added (eg.
				# Glideslope of 3.25 degrees on heading of 123.456 becomes
				# 325123.456)
				nav_bearing_true = str(list[6])
				nav_ident = str(list[7])
				apt_ident = str(list[8])
				rwy_ident = str(list[9])
				nav_name = str(list[10:listlen]).replace("', '", " ").replace("['","").replace("']","").replace("[]","")
				# specifier is not separated in xplane data, we need the last one
				nav_suffix = str(list[listlen-1])
				#insert_navaid(nav_ident,apt_ident,rwy_ident,nav_elev_ft,None,nav_freq_mhz,nav_bearing_true,None,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,None,None,None,nav_xplane_code)
			
			# Marker Beacon, Outer (OM), Middle (MM) and Inner (IM) Markers 
			if line.startswith("7 ") or line.startswith("8 ") or line.startswith("9 "):
				# [4] and [5] not used
				nav_bearing_true = str(list[6])
				# [7] not used
				apt_ident = str(list[8])
				rwy_ident = str(list[9])
				nav_name = None
				# specifier is not separated in xplane data, we need the last one
				nav_suffix = str(list[listlen-1])
				# Sorry, markers need an identifier, for database reasons
				marker_count += 1
				nav_ident = nav_suffix+str(marker_count)
				insert_navaid(nav_ident,apt_ident,rwy_ident,nav_elev_ft,None,None,nav_bearing_true,None,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,None,None,None,None,nav_xplane_code)
				
			# DME, Distance Measuring Equipment 
			if line.startswith("12 ") or line.startswith("13 "):
				nav_freq_mhz = str(list[4])
				nav_range_nm = str(list[5])
				nav_bias_nm = str(list[6])
				nav_ident = str(list[7])
				#apt_ident = str(list[8])
				#rwy_ident = str(list[9])
				nav_name = str(list[10:listlen]).replace("', '", " ").replace("['","").replace("']","").replace("[]","")
				# specifier is not separated in xplane data, we need the last one
				nav_suffix = str(list[listlen-1])
				# 12 = Suppress frequency = 1, 13 = display frequency = 0
				if line.startswith("12 "):
					nav_no_freq = "1"
				else:
					nav_no_freq = "0"
			
				# When DME-ILS there is apt identifier and runway number, but no name
				if nav_suffix == "DME-ILS":
					apt_ident = str(list[8])
					rwy_ident = str(list[9])
					nav_name = None
					
				else:
					apt_ident = None
					nav_name = str(list[8:listlen-1]).replace("', '", " ").replace("['","").replace("']","").replace("[]","")
				#insert_navaid(nav_ident,apt_ident,rwy_ident,nav_elev_ft,None,nav_freq_mhz,None,None,nav_name,nav_suffix,nav_center_lon84,nav_center_lat84,nav_range_nm,nav_bias_nm,None,nav_no_freq,nav_xplane_code)
			
		except:
			pass

	readnav.close()
	
fillthenav()

def postprocesscircles():
	# Doing geometry updates in navaid
	sqlnav = "SELECT * from navaid"
	cur.execute(sqlnav)
	allnav = cur.fetchall()
	conn.commit()

	countcircle = 0

	for rownav in allnav: 
	
		latsql = "SELECT nav_center_lat84,nav_center_lon84,nav_range_nm FROM navaid WHERE nav_ident='"+rownav[1]+"' AND nav_range_nm IS NOT NULL;"
		cur.execute(latsql)
		conn.commit()
	
		latlon = cur.fetchone()
		
		lat84 = latlon[0]
		lon84 = latlon[1]
		navrange = int(latlon[2])*1852 # getting the range in meter
	
		# Drawing the range polygons
	
		circlerange = drawcircle(navrange,lon84,lat84)
		thiscircles = circlerange[:-2]+"))"
		
		rangesql = "UPDATE navaid SET nav_range_poly=ST_Transform(ST_GeometryFromText('"+thiscircles+"', 4326),3857) WHERE nav_ident='"+rownav[1]+"';"
		cur.execute(rangesql)
		conn.commit()
	
		countcircle += 1
		print "Drawing circles for navaid range: "+str(rownav[1])+" "+str(countcircle)

#postprocesscircles()

conn.close()



endtime = time.asctime()

with open("import_xplane_navaid.log", "a") as log:
	log.write("Import finished: "+endtime+"\n")
	log.close()

	