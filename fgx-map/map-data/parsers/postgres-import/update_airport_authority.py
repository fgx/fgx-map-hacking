#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import sys, csv, psycopg2, yaml


conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']

conn = psycopg2.connect(connectstring)
cur = conn.cursor()

def updateauthority(apt_ident):
	sql = "UPDATE airport SET apt_authority='mil' WHERE apt_ident LIKE '"+apt_ident+"';"
	cur.execute(sql)
	conn.commit()
	
def readourairports():
	reader = open("../../data/ourairports/airports.csv", 'rU')
	csvreader = csv.reader(reader)
	csvreader.next()
	
	counthowmany = 0

	for row in csvreader:
		
		termslist = ['Naval', 'Air Base', 'Airbase', 'Army', 'Military', 'Air Force', 'Airforce', 'RNZAF', 'AAF']
		
		for i in termslist:
			if i in row[3]:
				counthowmany += 1
				print "Update: "+row[1], row[3]
				updateauthority(row[1])
	
	
	print "Count: "+str(counthowmany)
				
	
	cur.close()
	conn.close()
	
readourairports()


