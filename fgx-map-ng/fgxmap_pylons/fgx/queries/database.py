
#from fgx import db
from fgx.model import meta

def tables(db):

	sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
	
	results = meta.Sess.__dict__[db].execute(sql).fetchall()
	
	ret = []
	for r in results:
		ret.append({'table': r[0]})
	
	return ret

def drop_table(table):
		
	sql = "drop table if exists %s;" % table

	meta.Session.execute(sql)
	meta.Session.commit()
	
	
	
def empty_table(table):
		
	sql = "delete from  %s;" % table
	meta.Session.execute(sql)
	meta.Session.commit()
	
	## Also delete stuff from nav_search
	if table in ['ndb', 'fix', 'vor', 'dme']:
		sql = "delete from nav_search where nav_type = '%s';" % table
		meta.Session.execute(sql)
		meta.Session.commit()
	
	
	
	
def columns(table):
	
	## IS this an injectin attack
	sql = "SELECT column_name, data_type, character_maximum_length, numeric_precision, is_nullable "
	sql += " FROM information_schema.columns WHERE table_name = '%s' " % table
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