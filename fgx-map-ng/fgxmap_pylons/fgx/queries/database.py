
#from fgx import db
from fgx.model.meta import Session

def tables():

	sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
	results = Session.execute(sql).fetchall()
	
	ret = []
	for r in results:
		ret.append({'table': r[0]})
	
	return ret

	
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
	results = Session.execute(sql).fetchall()
	
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