#!/usr/bin/python

import os, sys, json, psycopg2, psycopg2.extras

def get_airport(req, searchstring):
	req.content_type = 'text/html'
	collected = ""
	
	try:
		conn = psycopg2.connect("dbname=xplanedata1000 user=webuser password=password")
		cur = conn.cursor()

		#cur.execute("SELECT icao, name, ST_AsGeoJSON(wkb_geometry, 8, 1) FROM airports WHERE icao ||' '|| name LIKE (%s) LIMIT 50;", ["%"+searchstring+"%"])
		cur.execute("SELECT icao, name, ST_AsText(ST_Transform(wkb_geometry,4326)) FROM airports WHERE icao ||' '|| name LIKE (%s) LIMIT 50;", ["%"+searchstring+"%"])

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

	
	


