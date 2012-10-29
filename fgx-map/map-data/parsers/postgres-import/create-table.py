#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import psycopg2, yaml

conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

fields = open('airport.yaml')
airportMap = yaml.load(fields)
fields.close()

sqlstring = "CREATE TABLE airport ("

for i in airportMap.keys():
	if airportMap[i]['size'] == None:
		sqlstring += airportMap[i]['field'] + " " + airportMap[i]['type'] + ","# \\\n"
	else:
		sqlstring += airportMap[i]['field'] + " " + airportMap[i]['type'] + "(" + str(airportMap[i]['size']) + ")" + ","# \\\n"
	
sqlstring = sqlstring + ");"
exe = sqlstring.replace(",);",");")

print sqlstring

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']

conn = psycopg2.connect(connectstring)
cur = conn.cursor()
			
cur.execute("DROP TABLE IF EXISTS airport;")

cur.execute(exe)


conn.commit()
cur.close()
conn.close()

print "--- CREATED TABLE: AIRPORT ---"

