
#from fgx import db
from fgx.model import meta



def search(ident=None, search=None, nav_type=None, bounds=None):
	
	
	 ## The cols to return, this is a string with spces and split later
	cols_str = "navaid_pk ident name nav_type freq"
	
	## now we make the select.. parts
	sql, cols = meta.select_sql(cols_str)

	sql += ", ST_X(wkb_geometry) as lat,  ST_Y(wkb_geometry) as lon "
	cols.append("lat")
	cols.append("lon")
	
	## now the tables and joins
	sql += " from navaid  "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	sql += " where 1 = 1 "
	
	if bounds:
		sql += " and '((POINT(%s %s),(POINT(%s %s))'" % ()
		
	if search:
		sql += " and( ident ilike '%s' " % ("%" + search + "%")
		sql += " or name ilike '%s' " % ("%" + search + "%") + ")"
		
	if nav_type:
		sql += " and nav_type = '%s' " % nav_type.upper()
		
	if ident:
		sql += " and ident =  '%s' " % ident.upper()
		
	sql += "limit 100"
	
	return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	
	
	