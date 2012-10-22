#!/usr/bin/python

import os, sys, json, psycopg2, psycopg2.extras

def get_airport(req, searchstring):
	req.content_type = 'text/html'
	collected = ""
	
	try:
		conn = psycopg2.connect("dbname=xplanedata1000 user=webuser password=password")
		cur = conn.cursor()

		#cur.execute("SELECT icao, name, ST_AsGeoJSON(wkb_geometry, 8, 1) FROM airports WHERE icao ||' '|| name LIKE (%s) LIMIT 50;", ["%"+searchstring+"%"])
		cur.execute("SELECT airports.icao, airports.name, ST_AsText(ST_Transform(wkb_geometry,4326)) FROM \
					airports WHERE airports.icao ||' '|| airports.name  LIKE (%s) LIMIT 100;", ["%"+searchstring+"%"])

		
		output = cur.fetchall()
	
		conn.commit()
		cur.close()
		conn.close()
		
		
		
		for row in output:
			cl1 = row[2].replace("POINT(","")
			cl2 = cl1.replace(")", "")
			cl3 = "lon=" + cl2.replace(" ","&lat=")
			link = "<a href='http://map.fgx.ch/?zoom=12&" + cl3 + "&layers=B00FTFFFFFFF'>" + row[0] + "</a> " + row[1] + "<BR>"
			
			collected += link
			
		return collected
		
	
	except psycopg2.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)
    
	finally:
    
		if conn:
			conn.close()
	
def get_navaid(req, searchstring):
	req.content_type = 'text/html'
	
	try:
		conn = psycopg2.connect("dbname=xplanedata1000 user=webuser password=password")
		cur = conn.cursor()

		cur.execute("SELECT fix_name, ST_AsGeoJSON(wkb_geometry, 8, 1) FROM fix WHERE fix_name LIKE (%s) LIMIT 50;", ["%"+searchstring+"%"])

		output = cur.fetchall()
	
		conn.commit()

		cur.close()
		conn.close()
	
		return output
	
	except psycopg2.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)
    
	finally:
    
		if conn:
			conn.close()
			
			
def get_points(req, searchstring):
	req.content_type = 'text/html'
	collected = ""
	
	try:
		conn = psycopg2.connect("dbname=xplanedata1000 user=webuser password=password")
		cur = conn.cursor()

		cur.execute("SELECT ST_AsText(wkb_geometry) FROM airports WHERE icao ||' '|| name LIKE (%s) LIMIT 50;", ["%"+searchstring+"%"])

		output = cur.fetchall()
	
		conn.commit()
		cur.close()
		conn.close()
		
		for row in output:
			collected += str(row[0]) + ","
			
		return collected
		
		
	
	except psycopg2.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)
    
	finally:
    
		if conn:
			conn.close()
	
					
def get_airport_json(req, searchstring):
	req.content_type = 'application/json'
	collected = ""
	
	try:
		conn = psycopg2.connect("dbname=xplanedata1000 user=webuser password=password")
		cur = conn.cursor()

		cur.execute("SELECT row_to_json(row(icao,name, ST_AsText(wkb_geometry))) FROM airports WHERE icao ||' '|| name LIKE (%s) LIMIT 50;", ["%"+searchstring+"%"])
		
		output = cur.fetchall()
		
		
		rep01 = str(output).replace("\"f1\":","\"icao\":")
		rep02 = rep01.replace("\"f2\":","\"name\":")
		rep03 = rep02.replace("\"f3\":","\"geometry\":")
		rep04 = rep03.replace("',), ('","\n")
		rep05 = rep04.replace("[('","{\n\"success\": \"true\",\n\"airports\": [\n")
		rep06 = rep05.replace("',)]","]}")
		rep07 = rep06.replace("}\n{","},\n{")
	
		conn.commit()
		cur.close()
		conn.close()
		
		return rep07
		
		
	
	except psycopg2.DatabaseError, e:
		print 'Error %s' % e    
		sys.exit(1)
    
	finally:
    
		if conn:
			conn.close()

	
	


