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

def readourairports():
	reader = open("../../data/ourairports/airports.csv", 'rU')
	csvreader = csv.reader(reader)
	csvreader.next()
	
	conn = psycopg2.connect(connectstring)
	cur = conn.cursor()
	
	countupdate = 0

	for row in csvreader:
		apt_local_code = row[13]
		apt_country = row[8]
		apt_name_utf8_read = row[3]
		apt_name_utf8 = apt_name_utf8_read.replace("'", "’")
		
		sql3 = "UPDATE airport SET apt_country='"+apt_country+"', apt_local_code='"+apt_local_code+"', apt_name_utf8='"+apt_name_utf8+"' WHERE apt_ident LIKE '"+row[1]+"';"
		cur.execute(sql3)
		conn.commit()
		
		
	#for row1 in csvreader:
		
		what_ident = row[1]
		sql4 = "SELECT apt_ident,apt_name_ascii FROM airport WHERE apt_ident LIKE '"+what_ident+"';"
		cur.execute(sql4)
		conn.commit()
		
		fetchy = cur.fetchone()
		
		if fetchy != None:
			countupdate += 1
		
			ident_search = fetchy[0]
			name_search = fetchy[1].replace("'","’")
			
			#print ident_search, name_search
			sql5 = "UPDATE airport SET apt_search='"+ident_search+"' || '"+name_search+"' || '"+apt_local_code+"' || '"+apt_name_utf8+"' WHERE apt_ident='"+row[1]+"';"
			cur.execute(sql5)
			conn.commit()
		
		countupdate += 1
		print countupdate
		#print "--- Updated '"+apt_name_utf8+"' from ourairports data."

	cur.close()
	conn.close()
	
readourairports()


