

from fgx.model import meta

#SELECT st_y(wkb_geometry) as lat, st_x(wkb_geometry) as lon, ident FROM fix limit 10;


## Does an sql query and return a list of dict
def airports(search=None, bounds=None, apt_type=None, lookup=True):
 
    ## The cols to return, this is a string with spces and split later
	cols_str = "apt_ident apt_name apt_center_lon apt_center_lat"
	
	if lookup == False:
		## lookup returns short data, this is long so add other cols as required
		cols_str = " geometry, apt_xplane_code apt_foo apt_bar  "
	
	## now make and array
	##cols = cols_str.split(" ")
	
	## now we make the select.. parts
	sql, cols = meta.select_sql(cols_str)

	
	if 1 == 0: 
		## This block for demonstration prurposes
	
		## next we add some other mad queries.. and the col
		sql += ", foo as bar, some_funct(wkb_geometry) as  gral_special "
		cols.append("gral_special")
		
		## subquery for count
		sql += ", (select count(*) from runways where runways.apt_ident = airport.apt_ident) as rwy_count "
		cols.append("rwy_count")
	
	## now the tables and joins
	sql += " from airport "
	#sql += " inner join another_table on airport.apt_ident = another_table.apt_ident "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	sql += " where 1 = 1 "
	
	if bounds:
		sql += " and '((POINT(%s %s),(POINT(%s %s))'" % ()
		
	if search:
		sql += " and apt_ident ilike '%s' " % ("%" + search + "%")
		
	if apt_type:
		sql += " and apt_type l= %s" % apt_type
		
	
	return meta.query_to_dic(meta.Sess.data.execute(sql).fetchall(), cols)
	
	
	
	
	
