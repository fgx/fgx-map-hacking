
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
	
	sql = "SELECT column_name FROM information_schema.columns WHERE table_name = %(table)s "
	results = Session.execute(sql, table=table).fetchall()
	
	ret = []
	for r in results:
		ret.append({'database': r[0]})
	
	return ret