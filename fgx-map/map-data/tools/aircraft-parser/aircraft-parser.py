#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#
# Creating the aircraft list csv is a manual task, the tables coming from FAA/O are 
# not parseable in a beautyfulsoup manner, nore with this simple helper here. 
# There are too many HTML/table issues in JO 7110.65U. So It
# Here is the link: http://www.faa.gov/air_traffic/publications/atpubs/ATC/index.htm

import sys, csv, os, re, psycopg2

# Hm, I keep this snipplet below ATM. Because I will need it somewhere else.
# Please ignore. (Maybe you can use it instead of bs4, it’s ways faster to strip
# all the tags and put it into database without beautyfulsoup, in case you have
# an easy searchable html/attribute or xml structure.)

#from HTMLParser import HTMLParser

#class MLStripper(HTMLParser):
#    def __init__(self):
#        self.reset()
#        self.fed = []
#    def handle_data(self, d):
#        self.fed.append(d)
#    def get_data(self):
#        return ''.join(self.fed)

#def strip_tags(html):
#    s = MLStripper()
#    s.feed(html)
#    return s.get_data()

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python aircraft-parser.py <file.csv>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python aircraft-parser.py <file.csv>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]
reader = open(inputfile, 'r')


conn = psycopg2.connect("dbname=mydatabase user=myuser password=mypass")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS aircraft;")
cur.execute("CREATE TABLE aircraft (id serial PRIMARY KEY, \
			manufacturer varchar, \
			model varchar, \
			type_designator varchar, \
			engines varchar, \
			weight_class varchar, \
			climb_rate varchar, \
			descent_rate varchar, \
			srs varchar, \
			LAHSO_group);")

def insert_aircraft(manufacturer,
			model,
			type_designator,
			engines,
			weight_class,
			climb_rate,
			descent_rate,
			srs,
			LAHSO_group):
				
	sql = '''
		INSERT INTO aircraft (manufacturer, model, type_designator, engines, weight_class, climb_rate, descent_rate, srs, LAHSO_group)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''
	params = [manufacturer, model, type_designator, engines, weight_class, climb_rate, descent_rate, srs, LAHSO_group]
	cur.execute(sql, params)

	
def get_aircraft_list():

		reader = csv.reader(open(inputfile, "rU"),delimiter=';')
		for row in reader:
			insert_aircraft(row)
	
			
get_aircraft_list()

conn.commit()
cur.close()
conn.close()

print "Done."

