#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#
# Modified by Pete Morgan, Wales UK

import sys, psycopg2, yaml, yaml.constructor

from optparse import OptionParser


##======================================================================
## Parse Options
##======================================================================
usage = "usage: %prog -d db_connection.yaml [options] table_definition.yaml "
#usage += " commands: \n"
#usage += "    drop [tables] - eg drop fix ndb vor\n"


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

## Parse will crash out above first is some args missing <<<

## Check we got an arg for data def yaml file
if len(args) == 0:
	print "FATAL: need pull path to  'table_definition.yaml' file"
	parser.print_help()
	sys.exit(1)
	

##======================================================================
## Helper Functions
##======================================================================
def get_create_table_sql(tableDef, drop=True):


	cols = []
	for f in tableDef.fields:
		if f.size == None:
			cols.append( f.name + " " + f.type )
		else:
			cols.append( f.name + " " + f.type + "(" + str(f.size) + ")" )

	sqlstring = ""
	if drop:
		sqlstring = "DROP TABLE IF EXISTS "+ tob.table+";\n"
	
	sqlstring += "create table %s (" % tableDef.table 
	sqlstring += ", ".join(cols)
	sqlstring = sqlstring + ");\n"
	return sqlstring


	
##======================================================================
## Lets GO!
##======================================================================

## import config and connect db
import config
config.init_db(opts.connect_yaml)

## Load yaml with table def
table_def_yaml = args[0]
tob = config.load_yaml(table_def_yaml, as_object=True)
#print tob, tob.table

## Create the table
sql =  get_create_table_sql(tob, drop=True)
config.DB.execute(sql)
config.CONN.commit()

# All done
config.CONN.close()

print "--- CREATED TABLE: %s ---" % tob.table
print sql









