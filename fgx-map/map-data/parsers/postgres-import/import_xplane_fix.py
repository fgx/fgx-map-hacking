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



entrycount = 0


def insert_fix(fix_ident,\
			  fix_center_lon84,\
			  fix_center_lat84):
	"""
	fix_center = "POINT("+fix_center_lon84+" "+fix_center_lat84+")"
	
	sql = '''INSERT INTO fix (fix_ident,fix_center_lon84,fix_center_lat84,fix_center)
		VALUES (%s,%s,%s,ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	
	params = [fix_ident,fix_center_lon84,fix_center_lat84,fix_center]
	"""
	sql2 = "insert into fix(fix_ident,  fix_center) values('%s', ST_Transform(ST_GeomFromText('POINT(%s %s)', 4326),3857))" % (fix_ident, fix_center_lon84, fix_center_lat84)
	params2 = [fix_ident, fix_center_lon84, fix_center_lat84]
	#print "Inserted: "+fix_ident
	
	try:
	      #cur.execute(sql, params)
	      cur.execute(sql2, params2)
	except:
		print "Database Error, check sql and parameters.", sql2
		with open("import_xplane_fix.log", "a") as log:
			log.write("  error: " + sql2 +"\n")
			log.close()
		#sys.exit(0)
		
	#conn.commit()


def fillthefix():

	c = 0
	with open(inputfile) as readnav:
		for line in readnav:
			c += 1
			# Skip first three lines, hope Robin Peel will never change this behaviour ;-)
			if c < 4:
				#readnav.next()
				#readnav.next()
				#readnav.next()
				pass
			else:
			
				if not line.startswith("99"):
					lst = line.strip().split()
		
					#spaceremoved = " ".join(line.split())
					#lst = spaceremoved.split(" ")
					#listlen = len(lst)
					
					# Reaching the last line is getting a '99'
					
					#print lst
					#try:
					fix_center_lat84 = str(lst[0])
					fix_center_lon84 = str(lst[1])
					fix_ident = str(lst[2])
			
					# Hi Fix
					insert_fix(fix_ident,fix_center_lon84,fix_center_lat84)
						
					#except:
					#print '''Big problem with this line in data.
					#1) Check if it's valid geometry
					#2) Check if it's really a valid data line along specs'''
					if c % 1000 == 0:
						print c, lst
						conn.commit()
			#readnav.close()
	conn.commit()

## Delete existing
if True:	
	sqlnuke = "delete  from fix"
	cur.execute(sqlnuke)
	conn.commit()

## Create View
sql_view = """create or replace view v_fix as
SELECT 
  fix.fix_ident, 
  fix.fix_center,
  ST_Y(ST_Transform(fix.fix_center, 4326)) as fix_lat84,
  ST_X(ST_Transform(fix.fix_center, 4326)) as fix_lon84
  
FROM 
  fix"""
cur.execute(sql_view)
conn.commit()


## Iimport fix file
fillthefix()

def postprocesscoords():
	# Doing geometry updates in fix
	##sqlnav = "SELECT * from fix"
	##cur.execute(sqlnav)
	#allnav = cur.fetchall()
	#conn.commit()

	#for rownav in allnav: 
	#
	#	# query gives lon/lat (postgis x/y) as text for the center point in reprojected format
	sql2 = "UPDATE fix SET fix_center_lon=ST_X(fix_center), fix_center_lat=ST_Y(fix_center);"
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

	