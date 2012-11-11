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

	for row in csvreader:
		global apt_local_code
		apt_local_code = row[13]
		#print apt_local_code
		global apt_country
		apt_country = row[8]
		#print apt_country
		global apt_name_utf8
		apt_name_utf8_read = row[3]
		apt_name_utf8 = apt_name_utf8_read.replace("'", "’")
		#print apt_name_utf8
		
			
		sql3 = "UPDATE airport SET apt_country='"+apt_country+"', apt_local_code='"+apt_local_code+"', apt_name_utf8='"+apt_name_utf8+"' WHERE apt_gps_code='"+row[1]+"';"
		cur.execute(sql3)
		conn.commit()
		print "--- Updated '"+apt_name_utf8+"' with ourairports data."

	cur.close()
	conn.close()
	
readourairports()