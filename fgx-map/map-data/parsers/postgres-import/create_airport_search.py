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
	
	sql1 = "SELECT * FROM airport;"
	cur.execute(sql1)
	
	records = cur.fetchall()
	
	countsearch = 0
	
	for record in records:

		sql4 = "SELECT apt_ident,apt_local_code,apt_name_ascii,apt_name_utf8 FROM airport WHERE apt_ident='"+record[1]+"';"
		cur.execute(sql4)
		conn.commit()
		
		fetchy = cur.fetchone()
		
		#print fetchy
		
	#if fetchy != None:
		
		ident_search = fetchy[0]
		local_code_search = fetchy[1]
		name_ascii_search = fetchy[2].replace("'","’") # This is ugly, but E' doesn’t work properly, also with \' (?)
		name_utf8_search = fetchy[3]
		
		if local_code_search == None:
			local_code_search = ""
		if name_utf8_search == None:
			name_utf8_search = ""
		# Using E' for escaping ' derived by xplane in field apt_name_ascii
		# To be sure also using it in apt_name_utf8
		sql5 = "UPDATE airport SET apt_search='"+ident_search+"' || E'"+local_code_search+"' || E'"+name_ascii_search+"' || E'"+name_utf8_search+"' WHERE apt_ident='"+fetchy[0]+"';"
		cur.execute(sql5)
		conn.commit()
		
		countsearch += 1
		
		print "Updating: "+ident_search+" "+str(countsearch)

	cur.close()
	conn.close()
	
updatesearch()


