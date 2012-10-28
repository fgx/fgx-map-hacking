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

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']

conn = psycopg2.connect(connectstring)
cur = conn.cursor()
			
cur.execute("DROP TABLE IF EXISTS airport;")
cur.execute("CREATE TABLE airport (apt_id serial PRIMARY KEY, \
			apt_gps_code varchar, \
			apt_name_ascii varchar, \
			apt_elev_ft varchar, \
			apt_center geometry(Point,3857));")


conn.commit()
cur.close()
conn.close()

print "--- CREATED TABLE AIRPORT ---"

