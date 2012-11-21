
#from fgx import db
from fgx.model import meta
import sqlalchemy.orm

def tables(db_name):

	sel_db = meta.Base.__dict__[db_name].metadata.tables.keys()
	return [{"table": t} for t in sel_db]


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
	
	

	
def columns(db_name, table_name):
		
	cols = meta.Base.__dict__[db_name].metadata.tables[table_name].columns
	lst = []
	for c in  cols:
		print c, c.type
		
		lst.append( dict(column=c.name, type=str(c.type), nullable=c.nullable) )
	return lst
		
	## IS this an injectin attack
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