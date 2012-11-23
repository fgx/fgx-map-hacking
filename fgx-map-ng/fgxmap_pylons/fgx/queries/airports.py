

from fgx.model import meta
from fgx.model.data import Airport, Runway
#SELECT st_y(wkb_geometry) as lat, st_x(wkb_geometry) as lon, ident FROM fix limit 10;


## Does an sql query and return a list of dict
def airports(apt_ident=None, apt_name_ascii=None, bounds=None, apt_type=None, lookup=True):
 
    ## The cols to return, this is a string with spces and split later
	cols_str = "apt_ident apt_name_ascii apt_authority apt_size"
	

		
	## now we make the select.. parts
	sql, cols = meta.select_sql(cols_str)

	sql += ", ST_X(apt_center) as apt_center_lat,  ST_Y(apt_center) as apt_center_lon "
	cols.append("apt_center_lat")
	cols.append("apt_center_lon")
	## now the tables and joins
	sql += " from airport "
	#sql += " inner join another_table on airport.apt_ident = another_table.apt_ident "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	sql += " where 1 = 1 "
	
	if bounds:
		sql += " and '((POINT(%s %s),(POINT(%s %s))'" % ()
		
	if apt_ident:
		sql += " and apt_ident ilike '%s' " % ("%" + apt_ident + "%")
	if apt_name_ascii:
		sql += " and apt_name_ascii ilike '%s' " % ("%" + apt_name_ascii + "%")
		
		
	if apt_type:
		sql += " and apt_type l= %s" % apt_type
		
	
	return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	
	
	
## Does an sql query and return a list of dict
def airport(apt_ident):
 
    ## The cols to return, this is a string with spces and split later
	#cols_str = "apt_ident apt_name_ascii apt_authority apt_size "
	

		
	## now we make the select.. parts
	#sql, cols = meta.select_sql(cols_str)

	#sql += ", ST_X(apt_center) as apt_center_lat,  ST_Y(apt_center) as apt_center_lon "
	#cols.append("apt_center_lat")
	#cols.append("apt_center_lon")
	## now the tables and joins
	#sql += " from airport "
	#sql += " inner join another_table on airport.apt_ident = another_table.apt_ident "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	#sql += " where apt_ident  = '%s' " % apt_ident
		
	
	#return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	
	return [ob.dic() for ob in meta.Sess.data.query(Airport).filter_by(apt_ident=apt_ident).order_by(Airport.apt_ident).all() ]
	
	
## Does an sql query and return a list of dict
def runways(apt_ident):
 
    ## The cols to return, this is a string with spces and split later
	#cols_str = "apt_ident apt_name_ascii apt_authority apt_size "
	
	cols = ['rwy_ident', 'runway']
	
	sql = "select apt_ident, "
	sql += " rwy_ident || '-' || rwy_ident_end as rwy "
	sql += " from runway "
	 

		
	## now we make the select.. parts
	#sql, cols = meta.select_sql(cols_str)

	#sql += ", ST_X(apt_center) as apt_center_lat,  ST_Y(apt_center) as apt_center_lon "
	#cols.append("apt_center_lat")
	#cols.append("apt_center_lon")
	## now the tables and joins
	#sql += " from airport "
	#sql += " inner join another_table on airport.apt_ident = another_table.apt_ident "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	sql += " where apt_ident  = '%s' " % apt_ident
	
	#return [ob.dic() for ob in #meta.Sess.data.query(Runway).filter_by(apt_ident=apt_ident).order_by(Runway.rwy_ident).all() ]
	
	
	return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	
