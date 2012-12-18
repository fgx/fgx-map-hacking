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
   print "Usage: python import_xplane_fix.py <file.dat>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python import_xplane_fix.py <file.dat>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]

starttime = time.asctime()

with open("import_xplane_fix.log", "a") as log:
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


def insert_fix(fix_ident,\
			   fix_center_lon84,\
			   fix_center_lat84):
	
	fix_center = "POINT("+fix_center_lon84+" "+fix_center_lat84+")"
	
	sql = '''INSERT INTO fix (fix_ident,fix_center_lon84,fix_center_lat84,fix_center)
		VALUES (%s,%s,%s,ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	
	
	params = [fix_ident,fix_center_lon84,fix_center_lat84,fix_center]
	
	print "Inserted: "+fix_ident
	
	try:
		cur.execute(sql, params)
	except:
		print "Database Error, check sql and parameters."
	  
	conn.commit()


def fillthefix():

	# Skip first three lines, hope Robin Peel will never change this behaviour ;-)
	readnav.next()
	readnav.next()
	readnav.next()

	for line in readnav:
	
		spaceremoved = " ".join(line.split())
		list = spaceremoved.split(" ")
		listlen = len(list)
		
		# Reaching the last line is getting a '99'
		if not line.startswith("99"):
		
			try:
				fix_center_lat84 = str(list[0])
				fix_center_lon84 = str(list[1])
				fix_ident = str(list[2])
	
			# Hi Fix
				insert_fix(fix_ident,fix_center_lon84,fix_center_lat84)
				
			except:
				print '''Big problem with this line in data.
				1) Check if it's valid geometry
				2) Check if it's really a valid data line along specs'''

	readnav.close()
	
fillthefix()

def postprocesscoords():
	# Doing geometry updates in fix
	sqlnav = "SELECT * from fix"
	cur.execute(sqlnav)
	allnav = cur.fetchall()
	conn.commit()

	for rownav in allnav: 
	
		# query gives lon/lat (postgis x/y) as text for the center point in reprojected format
		sql2 = "UPDATE fix SET fix_center_lon=ST_X(fix_center), fix_center_lat=ST_Y(fix_center) WHERE fix_pk="+str(rownav[0])+";"
		cur.execute(sql2)
	
		conn.commit()

print "Starting to process coordinates ..."
postprocesscoords()

conn.close()

endtime = time.asctime()

with open("import_xplane_fix.log", "a") as log:
	log.write("Import finished: "+endtime+"\n")
	log.close()
	
print "Finished. Goodbye"

	