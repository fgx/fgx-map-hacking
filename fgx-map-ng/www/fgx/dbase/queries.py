
import datetime
import re

from fgx import db  #, cache


##==============================================================================
### DB 
def databases():
	
	
	sql = "SELECT datname FROM pg_database;"
	results = db.session.execute(sql).fetchall()
	print results
	
	ret = []
	for r in results:
		ret.append({'database': r[0]})
	
	return ret
	
		
	
	
##==============================================================================
## Tables. 
def tables(db_name=None):
	## TODO.. this is using current db session heh heh ..!! so db_name is mute and no effect atmo
	sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'";
	
	ret = []
	for row in db.session.execute(sql).fetchall():
		ret.append({'table': row[0]})
	return ret
	
	
	
def columns(table):
	
	sql = "SELECT column_name FROM information_schema.columns WHERE table_name ='" + table + "';"
		
	ret = []
	for row in db.session.execute(sql).fetchall():
		ret.append({'column': row[0]})
		
	#sql = "SELECT column_name FROM information_schema.columns WHERE table_name ='table';"
		 
	return ret
	
	