

from fgx import db

## We need to load add the files with models here so their registeres with sqlalchemy

from fgx.navaids.models import Fix

def create_all():
	
	print "Create All"
	db.create_all()
	
	
def drop_all_tables():
	
	print "Drop All"
	db.drop_all()
	
	
	
def drop_table(table):
	
	print "Drop: %s" % table
	
	sql = " drop table if exists %s; " % table
	
	conn = db.session.connection()
	conn.execute(sql)
	db.session.commit()

	
	