
#from fgx import db
from fgx.model import meta



def search(ident=None, search=None, nav_type=None, bounds=None, ifr=False):
	
	
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
		
	if ifr:
		sql += " and (nav_type='FIX' or nav_type='VOR') "
		
	sql += "limit 100"
	
	return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	
	
	
def airways(search=None, awy=None):
	 ## The cols to return, this is a string with spces and split later
	#cols_str = "airway ident_entry ident_exit "
	
	## now we make the select.. parts
	#sql, cols = meta.select_sql(cols_str)

	"""
	sql += ", ST_X(ST_PointN(wkb_geometry, 1)) as lat1,  ST_Y(ST_PointN(wkb_geometry, 1)) as lon1 "
	cols.append("lat1")
	cols.append("lon1")
	
	sql += ", ST_X(ST_PointN(wkb_geometry, 2)) as lat2,  ST_Y(ST_PointN(wkb_geometry, 2)) as lon2 "
	cols.append("lat2")
	cols.append("lon2")
	"""
	## now the tables and joins
	sql = "select distinct(airway) as airway "
	cols = ['airway']
	
	sql += " from airway_segment  "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	sql += " where 1 = 1  "
	
	if search:
		sql += " and  airway ilike '%s' " % ("%" + search + "%") 
		##sql += " and  airway  not like '%-%' " # % ("%" + search + "%") 
	#if awy:
	#	sql += " airway = ANY(array['%s'])" % awy
		
	sql += " order by airway asc "
	lst = []
	for r in meta.Sess.data.execute(sql).fetchall():
		if r['airway'].find("-") == -1:
			lst.append({"airway": r['airway']})
		#sselse:
			
			
	return lst
	
	
def segments(awy):
	 ## The cols to return, this is a string with spces and split later
	cols_str = "airway ident_entry ident_exit fl_base fl_top level "
	
	## now we make the select.. parts
	sql, cols = meta.select_sql(cols_str)

	
	sql += ", ST_X(ST_PointN(wkb_geometry, 1)) as lat1,  ST_Y(ST_PointN(wkb_geometry, 1)) as lon1 "
	cols.append("lat1")
	cols.append("lon1")
	
	sql += ", ST_X(ST_PointN(wkb_geometry, 2)) as lat2,  ST_Y(ST_PointN(wkb_geometry, 2)) as lon2 "
	cols.append("lat2")
	cols.append("lon2")
	
	
	sql += " from airway_segment  "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	#sql += " where 1 = 1  "
	
	#if search:
	#	sql += " and  airway ilike '%s' " % ("%" + search + "%") 
	

	sql += " where  search ilike '%s' " % ("%" + "#" +  awy + "#" + "%") 
		
	#sql += " order by airway asc "
	return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	