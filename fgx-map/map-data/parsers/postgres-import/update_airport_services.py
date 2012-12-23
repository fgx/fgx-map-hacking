#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import sys, csv, os, re, psycopg2, yaml


conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']

conn = psycopg2.connect(connectstring)
cur = conn.cursor()

# Now take data from ourairports for various fields, if available

def updatesearch():
	
	conn = psycopg2.connect(connectstring)
	cur = conn.cursor()
	
	sql1 = "SELECT * FROM frequencies;"
	cur.execute(sql1)
	
	records = cur.fetchall()
	
	countsearch = 0
	
	for record in records:

		# When there is a xplane code 54 this means there is a tower frequency this means there is a tower
		# this means we can update apt_services in airport table with '1'. 'has_tower' is deprecated with
		# xplane format 1000, so this is a way to get this flag back.
		sql4 = "SELECT apt_ident FROM frequencies WHERE apt_ident='"+record[1]+"' AND frq_xplane_code='54';"
		cur.execute(sql4)
		conn.commit()
		
		fetchy = cur.fetchone()
		
		#print fetchy
		
		if fetchy != None:

			sql = "UPDATE airport SET apt_services='1' WHERE apt_ident='"+fetchy[0]+"';"
			cur.execute(sql)
			conn.commit()
		
			print "Updating: "+fetchy[0]
			
			countsearch += 1

	print "Updated: "+str(countsearch)+" airports with apt_services=1"

	cur.close()
	conn.close()
	
updatesearch()


