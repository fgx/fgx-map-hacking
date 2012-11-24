#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import sys, psycopg2, yaml, yaml.constructor

from optparse import OptionParser


# getting a ordered dict for yaml, you will  need ordereddict backport
# for python < 2.7
#
# ............................................................................
# The yaml ordered dict code is adapted from code gisted by Eric Naeseth, 2011

usage = "usage: %prog -d db_connection.yaml [options] table_definition.yaml "
#usage += " commands: \n"
#usage += "    drop [tables] - eg drop fix ndb vor\n"
#usage += "    dropall - Drops ALL database tables\n"
#usage += "    import [fix|ndb|vor|nav|apt|all] eg ./%prog import fix apt vor\n"

parser = OptionParser(usage=usage)

parser.add_option("-c", 
					action="store", dest="connect_yaml",
					help="Yaml file with database connection details"
                  )
                  
parser.add_option("-v", nargs=1,
					action="store", type="int", dest="verbose", default=1,
					help="Prints more verbose output 0-4 (0=none, 4=loads)"
                  )
(opts, args) = parser.parse_args()

## Parse will crash out above first <<<

## Check we got an arg for data def yaml file
if len(args) == 0:
	print "FATAL: need pull path to  'table_definition.yaml' file"
	parser.print_help()
	sys.exit(1)
	
	
## Shell config will validate dome things
import config
config.init(opts.connect_yaml)


table_def_yaml = args[0]


table_def = config.load_yaml(table_def_yaml)


"""
print "COLS="
for c  in data['cols']:
	print c

sys.exit(0)



conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

fields = open(table+".yaml")
tableMap = yaml.load(fields, OrderedDictYAMLLoader)
fields.close()
"""

class Table:

	def __init__(self, data):
		
		self.D = data
		print "TABLE", data
		
	def create_sql(self):
		
		sqlstring = "CREATE TABLE "+table+" ("

		for i in tableMap.keys():
			if tableMap[i]['size'] == None:
				sqlstring += tableMap[i]['field'] + " " + tableMap[i]['type'] + ","# \\\n"
			else:
				sqlstring += tableMap[i]['field'] + " " + tableMap[i]['type'] + "(" + str(tableMap[i]['size']) + ")" + ","# \\\n"
			
		sqlstring = sqlstring + ");"
		exe = sqlstring.replace(",);",");")

		print sqlstring

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']
if "host" in confMap:
	connectstring += " host=%s" % confMap['host']
conn = psycopg2.connect(connectstring)
cur = conn.cursor()
			
cur.execute("DROP TABLE IF EXISTS "+table+";")

cur.execute(exe)

conn.commit()
cur.close()
conn.close()

print "--- CREATED TABLE: "+table+" ---"










