

from fgx.model import meta

#SELECT st_y(wkb_geometry) as lat, st_x(wkb_geometry) as lon, ident FROM fix limit 10;


## Does an sql query and return a list of dict
def airports(apt_ident=None, apt_name_ascii=None, bounds=None, apt_type=None, lookup=True):
 
    ## The cols to return, this is a string with spces and split later
	cols_str = "apt_ident apt_name_ascii apt_center_lon apt_center_lat apt_authority apt_size"
	
	if lookup == False:
		## lookup returns short data, this is long so add other cols as required
		cols_str = " geometry, apt_xplane_code apt_foo apt_bar  "
		
	## now we make the select.. parts
	sql, cols = meta.select_sql(cols_str)

	
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
	
	
	
	
	
