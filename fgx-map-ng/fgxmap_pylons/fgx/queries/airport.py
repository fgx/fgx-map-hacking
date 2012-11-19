

## Does an sql query and return a list of dict
def airport(search=None, within=None, type="all", lookup=True):
 
    ## The cols to return, this is a string with spces and split later
	cols_str = "apt_ident apt_code apt_name apt_name apt_center_lon apt_center_lat"
	
	if lookup == False:
		## lookup returns short data, this is long so add other cols as required
		cols_str = " geometry, apt_xplane_code apt_foo apt_bar  "
	
	## now make and array
	cols = cols_str.split(" ")
	
	## now we make the select.. parts
	sql = "select %s " % ",".cols_str.split(" ") 

	## next we add some other mad queries.. and the col
	sql += ", foo as bar, some_funct(wkb_geometry) as  gral_special "
	cols.append("gral_special")
	
	## subquery for count
	sql += ", (select count(*) from runways where runways.apt_ident = airport.apt_ident) as rwy_count "
	cols.append("rwy_count")
	
	## now the tables and joins
	sql += " from airport "
	sql += " inner join another_table on airport.apt_ident = another_table.apt_ident "
	
	
	##  add the filters, we where 1 = 1 to make queries esier with and's
	sql += " where 1 = 1 "
	
	if within:
		sql += " and <geoery_function %s %s>" % (within.x, within.y etc)
		
	if search:
		sql += " and apt_ident like %s>" % search
		
	if apt_type != "all":
		sql += " and apt_type l= %s" % apt_type
		
	## Now get from database
	results = Session.execute(sql)
	
	return_list = []
	for r in results:
		dic = {}
		for c in cols:
			dic[c] = r[index.of(c)]
		return_list.append(dic)
			
	return return_list
	
	
	
	
	