
#from fgx import db
from fgx.model import meta
import sqlalchemy.orm

def tables(db_name):

	sel_db = meta.Base.__dict__[db_name].metadata.tables.keys()
	return [{"table": t} for t in sorted(sel_db)]


def drop_table(table):
		
	sql = "drop table if exists %s;" % table

	if table in ['navaid', 'airport']:
		meta.Sess.data.execute(sql)
		meta.Sess.data.commit()
	
	
	
def empty_table(table):
		
	sql = "delete from  %s;" % table
	meta.Session.execute(sql)
	meta.Session.commit()
	
	## Also delete stuff from nav_search
	if table in ['ndb', 'fix', 'vor', 'dme']:
		sql = "delete from nav_search where nav_type = '%s';" % table
		meta.Session.execute(sql)
		meta.Session.commit()
	
	

##@brief Returns a list of dict with the columns defininitions
#
# @param db_name database connection
# @param table_name The table to query columns for
def columns(db_name, table_name):
		
	cols = meta.Base.__dict__[db_name].metadata.tables[table_name].columns
	lst = []
	for c in cols:		
		lst.append( dict(column=c.name, type=str(c.type), nullable=c.nullable) )
	return lst
		
	## TODO integrate Olde flavour  below
	#sql = "SELECT column_name, data_type, character_maximum_length, numeric_precision, is_nullable "
	#sql += " FROM information_schema.columns WHERE table_name = '%s' " % table
	"""
	results = Session.execute(
		"SELECT column_name FROM information_schema.columns WHERE table_name = %(table)s ",
		dict(table=table)
	).fetchall()
	"""
	results = meta.Session.execute(sql).fetchall()
	
	ret = []
	for r in results:
		ret.append({'column': r[0], 
					'type': r[1],
					'max_char': r[2],
					'int_type': r[3],
					'nullable': r[4],
					'default': ' todo'
					})
	
	return ret