#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import sys, time, datetime, csv, os, re, psycopg2, yaml, warnings

 

# geographiclib 1.24 by (c) Charles Karney
from geographiclib.geodesic import Geodesic

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python import_xplane.py <file.dat>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python import_xplane.py <file.dat>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]

log = open("import_xplane.log", 'w')

temp_sql = open("temp_sql.txt", 'w')

starttime = time.asctime()
log.write("Import started: "+starttime+"\n")

conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']
if "host" in confMap:
	connectstring += " host=%s" % confMap['host']
conn = psycopg2.connect(connectstring)
cur = conn.cursor()

pointscollected = ""
runwaycount = 0
rwy_len_collect = []
apt_max_rwy_len_ft = 0
apt_min_rwy_len_ft = 0
apt_size = ""
lightingcollected = []
apt_ifr = "0"
apt_center_lon = ""
apt_center_lat = ""
apt_authority = ""
apt_services = ""
apt_country = ""
apt_name_utf8 = ""
apt_local_code = ""
bcn_type = ""
	
# Collect runway points to insert airport center with ST_Centroid for all runway points,
# collect runway length to insert min/max runway length (feet)
def collecting(points, rwy_len, rwy_app_lighting):
	global pointscollected
	pointscollected += points
	
	global runwaycount
	runwaycount += 1
	
	global rwy_len_collect
	rwy_len_collect.append(rwy_len)
	
	# Check if there is an approach light and indicate if IFR is available or not
	# Needs to be discussed this one
	global lightingcollected
	lightingcollected += rwy_app_lighting

	#print rwy_len_collect

# Look for min/max runway length in rwy_len_collect
# prepared for a more sophisticated list type
def get_rwy_min_max(rwy_len_collect):

	how_many_large_rwy = 0
	
	lenlist = zip(rwy_len_collect)
	
	global apt_max_rwy_len_ft
	global apt_min_rwy_len_ft
	apt_max_rwy_len_ft = int(round(float(map(max, zip(*lenlist))[0])*3.048))
	apt_min_rwy_len_ft = int(round(float(map(min, zip(*lenlist))[0])*3.048))
	
	# Counting runways longer than 3200 meters / 9700 feet
	for i in rwy_len_collect:
		if int(float(i)*3.048) >= 9700:
			how_many_large_rwy += 1
	
	# 2 runways >= 3200 meter = large
	# at least 1 runway >= 3200 meter = medium
	# rest = small
	global apt_size
	if how_many_large_rwy >= 2:
		apt_size = "large"
	elif how_many_large_rwy >= 1:
		apt_size = "medium"
	else:
		apt_size = "small"
		
def get_ifr(lightingcollected):
	global apt_ifr
	for i in lightingcollected:
		if i != "0":
			apt_ifr = "1"
			
def get_authority(bcn_type):
	global apt_authority
	if bcn_type == "4":
		apt_authority = "mil"
	else:
		if apt_name_ascii.startswith("[X]"):
			apt_authority = "clo"
		else:
			apt_authority = "civ"

def get_freqline(line):
	global frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code
	frq_xplane_code = line[0:2]
	frq_freq = line[3:8]
	frq_freq_nice = str(round(float(frq_freq)/100, 3))
	frq_description_end = len(line)
	frq_description = line[9:frq_description_end-2]
	frq_range_nm = "50"
	frq_range_km = "92.6"
	
	return frq_xplane_code,frq_freq,frq_freq_nice,frq_description,frq_range_nm,frq_range_km
	
def drawcircle(rangerad,lon,lat):
    # We need 0 and 360 to close the polygon
	#global circlelist
	azi_list = range(0,360,1)
	circlelist = "LINESTRING("
	for i in azi_list:
		result = Geodesic.WGS84.Direct(float(lat),float(lon),i,float(rangerad))
		#return str(result["lat2"])+" "+str(result["lon2"])+","
		#return str(result["lat2"])+" "+str(result["lon2"])+","
		circlelist += str(result["lon2"])+" "+str(result["lat2"])+","
	
	# End point
	endpoint = str(Geodesic.WGS84.Direct(float(lat),float(lon),0,float(rangerad))["lon2"])+" "+str(Geodesic.WGS84.Direct(float(lat),float(lon),0,float(rangerad))["lat2"])
	
	circlelist += endpoint+")"
	print circlelist
	return circlelist
			
def insert_airport(apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type):

	lastcoma = len(pointscollected)-1
	pointscollected2 = pointscollected[0:lastcoma] 
	
	apt_center = "MULTIPOINT ("+pointscollected2+")"
	
	apt_rwy_count = runwaycount
	
	# Geometry is reprojected to EPSG:3857, should become a command line parameter
	sql = '''
		INSERT INTO airport (apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type, apt_rwy_count, apt_min_rwy_len_ft, apt_max_rwy_len_ft, apt_size, apt_xplane_code, apt_ifr, apt_authority, apt_services, apt_center)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Centroid(ST_Transform(ST_GeomFromText(%s, 4326),3857)))'''
		
	#ST_Y(ST_Transform(apt_center,3857)),ST_X(ST_Transform(apt_center,3857)),ST_Y(ST_Transform(apt_center,4326)),ST_X(ST_Transform(apt_center,4326))
	#print sql
	
	params = [apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type, apt_rwy_count, apt_min_rwy_len_ft, apt_max_rwy_len_ft, apt_size, apt_xplane_code, apt_ifr, apt_authority, apt_services, apt_center]
	cur.execute(sql, params)
	
	# query gives lon/lat (postgis x/y) as text for the center point in reprojected format
	sql2 = "UPDATE airport SET apt_center_lon=ST_X(apt_center), apt_center_lat=ST_Y(apt_center) WHERE apt_ident='"+apt_ident+"';"
	cur.execute(sql2)
	
	# query gives lon/lat (postgis x/y) as text for the center point in WGS84 format
	sql3 = "UPDATE airport SET apt_center_lon84=ST_X(ST_Transform(apt_center,4326)), apt_center_lat84=ST_Y(ST_Transform(apt_center,4326)) WHERE apt_ident='"+apt_ident+"';"
	cur.execute(sql3)
	
def insert_runway(apt_ident,\
				rwy_ident,\
				rwy_ident_end,\
				rwy_width,\
				rwy_lon,\
				rwy_lat,\
				rwy_lon_end,\
				rwy_lat_end,\
				rwy_len_feet,\
				rwy_len_meters,\
				rwy_hdg,\
				rwy_hdg_end, \
				rwy_surface,\
				rwy_shoulder,\
				rwy_smoothness,\
				rwy_centerline_lights,\
				rwy_edge_lighting,\
				rwy_auto_dist_signs,\
				rwy_threshold,\
				rwy_overrun,\
				rwy_marking,\
				rwy_app_lighting,\
				rwy_tdz_lighting,\
				rwy_reil,\
				rwy_threshold_end,\
				rwy_overrun_end,\
				rwy_marking_end,\
				rwy_app_lighting_end,\
				rwy_tdz_lighting_end,\
				rwy_reil_end,\
				rwy_xplane_code,\
				A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon):
				
	# Coordinate ordering is (x, y) -- that is (lon, lat)
	# Polygon needs to be closed, repeating starting point
	rwy_poly = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
	#print rwy_polygon
	
	# Geometry is reprojected to EPSG:3857
	sql = '''
		INSERT INTO runway (apt_ident, rwy_ident, rwy_ident_end, rwy_width, rwy_lon, rwy_lat, rwy_lon_end, rwy_lat_end, rwy_len_feet, rwy_len_meters, rwy_hdg, rwy_hdg_end, rwy_surface,rwy_shoulder,rwy_smoothness,rwy_centerline_lights,rwy_edge_lighting,rwy_auto_dist_signs,rwy_threshold,rwy_overrun,rwy_marking,rwy_app_lighting,rwy_tdz_lighting,rwy_reil,rwy_threshold_end,rwy_overrun_end,rwy_marking_end,rwy_app_lighting_end,rwy_tdz_lighting_end,rwy_reil_end, rwy_xplane_code, rwy_poly)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	params = [apt_ident, rwy_ident, rwy_ident_end, rwy_width, rwy_lon, rwy_lat, rwy_lon_end, rwy_lat_end, rwy_len_feet, rwy_len_meters, rwy_hdg, rwy_hdg_end, rwy_surface,rwy_shoulder,rwy_smoothness,rwy_centerline_lights,rwy_edge_lighting,rwy_auto_dist_signs,rwy_threshold,rwy_overrun,rwy_marking,rwy_app_lighting,rwy_tdz_lighting,rwy_reil,rwy_threshold_end,rwy_overrun_end,rwy_marking_end,rwy_app_lighting_end,rwy_tdz_lighting_end,rwy_reil_end,rwy_xplane_code, rwy_poly]
	
	#print  cur.mogrify(sql, params) 
	
	cur.execute(sql, params)
	
	points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
	
	
def insert_waterway(apt_ident,\
				wwy_ident,\
				wwy_ident_end,\
				wwy_width,\
				wwy_lon,\
				wwy_lat,\
				wwy_lon_end,\
				wwy_lat_end,\
				wwy_len_feet,\
				wwy_len_meters,\
				wwy_hdg,\
				wwy_hdg_end, \
				wwy_buoys,\
				wwy_xplane_code,\
				A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon):
				
	# Coordinate ordering is (x, y) -- that is (lon, lat)
	# Polygon needs to be closed, repeating starting point
	wwy_poly = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
	#print wwy_polygon
	
	# Geometry is reprojected to EPSG:3857
	sql = '''
		INSERT INTO waterway (apt_ident, wwy_ident, wwy_ident_end, wwy_width, wwy_lon, wwy_lat, wwy_lon_end, wwy_lat_end, wwy_len_feet, wwy_len_meters, wwy_hdg, wwy_hdg_end, wwy_buoys, wwy_xplane_code, wwy_poly)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	params = [apt_ident, wwy_ident, wwy_ident_end, wwy_width, wwy_lon, wwy_lat, wwy_lon_end, wwy_lat_end, wwy_len_feet, wwy_len_meters, wwy_hdg, wwy_hdg_end, wwy_buoys,wwy_xplane_code, wwy_poly]
	cur.execute(sql, params)
	
	points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","			
	
def insert_helipad(apt_ident,\
				pad_ident,\
				pad_lon,\
				pad_lat,\
				pad_lon_end,\
				pad_lat_end,\
				pad_hdg,\
				pad_hdg_end,\
				pad_len_m,\
				pad_len_ft,\
				pad_width_m,\
				pad_width_ft,\
				pad_surface,\
				pad_marking,\
				pad_shoulder,\
				pad_edge_lighting,\
				pad_app_lighting,\
				pad_xplane_code,\
				A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon):
				
	# Coordinate ordering is (x, y) -- that is (lon, lat)
	# Polygon needs to be closed, repeating starting point
	pad_poly = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
	#print wwy_polygon
	
	# Geometry is reprojected to EPSG:3857
	sql = '''
		INSERT INTO helipad (apt_ident, pad_ident, pad_lon, pad_lat, pad_lon_end, pad_lat_end, pad_hdg, pad_hdg_end, pad_len_m, pad_len_ft, pad_width_m, pad_width_ft, pad_surface, pad_marking, pad_shoulder, pad_edge_lighting, pad_app_lighting, pad_xplane_code, pad_poly)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	params = [apt_ident, pad_ident, pad_lon, pad_lat, pad_lon_end, pad_lat_end, pad_hdg, pad_hdg_end, pad_len_m, pad_len_ft, pad_width_m, pad_width_ft, pad_surface, pad_marking, pad_shoulder, pad_edge_lighting, pad_app_lighting, pad_xplane_code, pad_poly]
	cur.execute(sql, params)
	
	points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","	

def insert_freq(apt_ident,\
				frq_type,\
				frq_freq,\
				frq_freq_nice,\
				frq_description,\
				frq_range_km,\
				frq_range_nm,\
				frq_xplane_code):
	
	sql = '''
		INSERT INTO frequencies (apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
	params = [apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code]
	
	cur.execute(sql, params)

def readxplane():
	reader = open(inputfile, 'r')
	
	
	print "Processing "+inputfile+" ..."
	log.write("Processing "+inputfile+" ...\n")
	
	reader.next()
	reader.next()
	reader.next()
	reader.next()
	
	print "First 4 lines of apt.dat skipped."
	log.write("First 4 lines of apt.dat skipped.\n")
	
	for line in reader:
		
		global apt_ident
		global apt_name_ascii
		global apt_elev_ft
		global apt_elev_m
		global apt_type
		global apt_xplane_code

		
		# airport line
		if line.startswith("1  "):
		
			apt_xplane_code_read = line[0]+line[1]
			apt_elev_ft_read = line[5]+line[6]+line[7]+line[8]+line[9]
			apt_deprecated1 = line[11]
			apt_deprecated2 = line[13]
			apt_ident_read = line[15]+line[16]+line[17]+line[18]
			
			tilend = len(line)
			apt_name_ascii_read = line[20:tilend-2]
						
			apt_ident = apt_ident_read
			apt_name_ascii = apt_name_ascii_read
			apt_elev_ft = apt_elev_ft_read
			apt_elev_m = int(float(apt_elev_ft_read)*0.3048)
			apt_type = "land"
			apt_xplane_code = apt_xplane_code_read
			
		if line.startswith("16 "):
		
			apt_xplane_code_read = line[0]+line[1]
			apt_elev_ft_read = line[5]+line[6]+line[7]+line[8]+line[9]
			apt_deprecated1 = line[11]
			apt_deprecated2 = line[13]
			apt_ident_read = line[15]+line[16]+line[17]+line[18]
			
			tilend = len(line)
			apt_name_ascii_read = line[20:tilend-2]
						
			apt_ident = apt_ident_read
			apt_name_ascii = apt_name_ascii_read
			apt_elev_ft = apt_elev_ft_read
			apt_elev_m = int(float(apt_elev_ft_read)*0.3048)
			apt_type = "sea"
			apt_xplane_code = apt_xplane_code_read
			
		if line.startswith("17 "):
		
			apt_xplane_code_read = line[0]+line[1]
			apt_elev_ft_read = line[5]+line[6]+line[7]+line[8]+line[9]
			apt_deprecated1 = line[11]
			apt_deprecated2 = line[13]
			apt_ident_read = line[15]+line[16]+line[17]+line[18]
			
			tilend = len(line)
			apt_name_ascii_read = line[20:tilend-2]
						
			apt_ident = apt_ident_read
			apt_name_ascii = apt_name_ascii_read
			apt_elev_ft = apt_elev_ft_read
			apt_elev_m = int(float(apt_elev_ft_read)*0.3048)
			apt_type = "heli"
			apt_xplane_code = apt_xplane_code_read
		
		# runways, we need it for some calculation, i.e. centerpoint
		# but also for getting shortest/longest runway, to set the apt_ifr
		# flag and much more
		if line.startswith("100 "):
		
			rwy_ident = str(line[31:34])
			rwy_ident_end = str(line[87:90])
		
			rwy_xplane_code = line[0:3]
			rwy_width =  line[5:13]
			rwy_surface = line[14:16].replace(" ","")
			rwy_shoulder = line[17:19].replace(" ","")
			rwy_smoothness = line[20:24]
			rwy_centerline_lights = line[25]
			rwy_edge_lighting = line[27]
			rwy_auto_dist_signs = line[29]
			rwy_number = str(line[31:34])
			rwy_lat = line[34:47]
			rwy_lon = line[48:61]
			rwy_threshold = line[62:69]
			rwy_overrun = line[70:77]
			rwy_marking = line[78:79]
			rwy_app_lighting = line[81:82]
			rwy_tdz_lighting = line[83]
			rwy_reil = line[85]
			rwy_number_end = str(line[87:90])
			rwy_lat_end = line[90:103]
			rwy_lon_end = line[104:117]
			rwy_threshold_end = line[119:125]
			rwy_overrun_end = line[126:133]
			rwy_marking_end = line[134:135]
			rwy_app_lighting_end = line[136:138].replace(" ","")
			rwy_tdz_lighting_end = line[139]
			rwy_reil_end = line[141]
			
			# Now some additional data, not in apt.dat
			
			# The NZSP problem
			if apt_ident == "NZSP":
				if rwy_lat_end > -90.0:
					rwy_lat_end = ( float(rwy_lat_end) + 90.0 )*-1.0
					log.write("NZSP problem solved in airport "+apt_ident+", runway "+rwy_number+"\n")
				if rwy_lat > -90.0:
					rwy_lat = ( float(rwy_lat) + 90.0 )*-1.0
					log.write("NZSP problem solved in airport "+apt_ident+", runway "+rwy_number+"\n")
			
			rwy_length = Geodesic.WGS84.Inverse(float(rwy_lat), float(rwy_lon), float(rwy_lat_end), float(rwy_lon_end))
			rwy_len_meters = str(rwy_length.get("s12"))
			
			rwy_len_feet = rwy_length.get("s12")*3.048
			
			rwy_hdg = rwy_length.get("azi2")
			
		
			rwy_length_end = Geodesic.WGS84.Inverse(float(rwy_lat_end), float(rwy_lon_end), float(rwy_lat), float(rwy_lon))
			rwy_hdg_end = str(360.0 + rwy_length_end.get("azi2"))
			
			rwy_threshold_direct = Geodesic.WGS84.Direct(float(rwy_lat),float(rwy_lon),float(rwy_hdg),float(rwy_threshold))
			rwy_threshold_direct_end = Geodesic.WGS84.Direct(float(rwy_lat_end),float(rwy_lon_end),rwy_length_end.get("azi2"),float(rwy_threshold_end))

			# Calculating runway points
			rwy_direct_A = Geodesic.WGS84.Direct(float(rwy_lat),float(rwy_lon),float(rwy_hdg-90.0),(float(rwy_width))/2)
			A_lat = rwy_direct_A.get("lat2")
			A_lon = rwy_direct_A.get("lon2")
			
			rwy_direct_B = Geodesic.WGS84.Direct(float(rwy_lat),float(rwy_lon),float(rwy_hdg+90.0),(float(rwy_width))/2)
			B_lat = rwy_direct_B.get("lat2")
			B_lon = rwy_direct_B.get("lon2")
			
			rwy_direct_C = Geodesic.WGS84.Direct(float(rwy_lat_end),float(rwy_lon_end),-360.0 + float(rwy_hdg_end)-90.0,(float(rwy_width))/2)
			C_lat = rwy_direct_C.get("lat2")
			C_lon = rwy_direct_C.get("lon2")
			
			rwy_direct_D = Geodesic.WGS84.Direct(float(rwy_lat_end),float(rwy_lon_end),-360.0 + float(rwy_hdg_end)+90.0,(float(rwy_width))/2)
			D_lat = rwy_direct_D.get("lat2")
			D_lon = rwy_direct_D.get("lon2")
			
			# Collecting runway points
			points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
			collecting(points, rwy_len_meters, rwy_app_lighting)
			
			insert_runway(apt_ident,rwy_ident,rwy_ident_end,rwy_width,rwy_lon,rwy_lat,rwy_lon_end,rwy_lat_end,rwy_len_meters,rwy_len_feet,rwy_hdg,rwy_hdg_end,rwy_surface,rwy_shoulder,rwy_smoothness,rwy_centerline_lights,rwy_edge_lighting,rwy_auto_dist_signs,rwy_threshold,rwy_overrun,rwy_marking,rwy_app_lighting,rwy_tdz_lighting,rwy_reil,rwy_threshold_end,rwy_overrun_end,rwy_marking_end,rwy_app_lighting_end,rwy_tdz_lighting_end,rwy_reil_end,rwy_xplane_code,\
			A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon)
			
			
		# WATER runways
		if line.startswith("101 "):
		
			wwy_xplane_code = line[0:3]
			wwy_width =  line[4:11]
			wwy_buoys = line[12:13]
			wwy_ident = str(line[14:16])
			wwy_lat = line[17:31]
			wwy_lon = line[32:45]
			
			wwy_ident_end = str(line[46:48])
			wwy_lat_end = line[49:62]
			wwy_lon_end = line[63:79]
			
			wwy_app_lighting = "0"
			
			# Now some additional data, not in apt.dat
			
			wwy_len = Geodesic.WGS84.Inverse(float(wwy_lat), float(wwy_lon), float(wwy_lat_end), float(wwy_lon_end))
			wwy_len_meters = str(wwy_len.get("s12"))
			
			#print "Meters: "+wwy_len_meters
			
			wwy_len_feet = wwy_len.get("s12")*3.048
			
			wwy_hdg = wwy_len.get("azi2")
			
			wwy_len_end = Geodesic.WGS84.Inverse(float(wwy_lat_end), float(wwy_lon_end), float(wwy_lat), float(wwy_lon))
			wwy_hdg_end = str(360.0 + wwy_len_end.get("azi2"))

			# Calculating runway points
			wwy_direct_A = Geodesic.WGS84.Direct(float(wwy_lat),float(wwy_lon),float(wwy_hdg-90.0),(float(wwy_width))/2)
			A_lat = wwy_direct_A.get("lat2")
			A_lon = wwy_direct_A.get("lon2")
			
			wwy_direct_B = Geodesic.WGS84.Direct(float(wwy_lat),float(wwy_lon),float(wwy_hdg+90.0),(float(wwy_width))/2)
			B_lat = wwy_direct_B.get("lat2")
			B_lon = wwy_direct_B.get("lon2")
			
			wwy_direct_C = Geodesic.WGS84.Direct(float(wwy_lat_end),float(wwy_lon_end),-360.0 + float(wwy_hdg_end)-90.0,(float(wwy_width))/2)
			C_lat = wwy_direct_C.get("lat2")
			C_lon = wwy_direct_C.get("lon2")
			
			wwy_direct_D = Geodesic.WGS84.Direct(float(wwy_lat_end),float(wwy_lon_end),-360.0 + float(wwy_hdg_end)+90.0,(float(wwy_width))/2)
			D_lat = wwy_direct_D.get("lat2")
			D_lon = wwy_direct_D.get("lon2")
			
			# Collecting runway points
			points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
			collecting(points, wwy_len_meters, wwy_app_lighting)
			
			insert_waterway(apt_ident,wwy_ident,wwy_ident_end,wwy_width,wwy_lon,wwy_lat,wwy_lon_end,wwy_lat_end,wwy_len_meters,wwy_len_feet,wwy_hdg,wwy_hdg_end,wwy_buoys,wwy_xplane_code,\
			A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon)
			
		# HELIPADS, we need it for heliport calculation, i.e. centerpoint
		# but we dont want to take this points into account for regular airports
		# so we look out for (H)
		if line.startswith("102 "):
		
			pad_xplane_code = line[0:3]
			pad_ident = str(line[4:6])
			pad_lat_read = line[7:19]
			pad_lon_read = line[21:33]
			pad_hdg = line[34:41]
			pad_len_m = line[42:49]
			pad_width_m = line[50:57]
			pad_surface = line[58:61]
			pad_marking = line[61:63]
			pad_shoulder = line[65:67]
			pad_smoothness = line[68:72]
			pad_edge_lighting = line[73]
			
			pad_app_lighting = "0"
			
			# Now some additional data, not in apt.dat
			
			# We get the centerpoint of the pad, but we want the center point at shape start, 
			# to get it calculated like runways and to prevent me from writing all separated for pads
			pad_direct = Geodesic.WGS84.Direct(float(pad_lat_read),float(pad_lon_read),float(pad_hdg)-180.0,(float(pad_len_m))/2)
			pad_lat = pad_direct.get("lat2")
			pad_lon = pad_direct.get("lon2")
			
			pad_direct_end = Geodesic.WGS84.Direct(float(pad_lat_read),float(pad_lon_read),float(pad_hdg),(float(pad_len_m)))
			pad_lat_end = pad_direct_end.get("lat2")
			pad_lon_end = pad_direct_end.get("lon2")
			
			pad_len = Geodesic.WGS84.Inverse(float(pad_lat), float(pad_lon), float(pad_lat_end), float(pad_lon_end))
			pad_len_m = str(pad_len.get("s12"))
			
			#print "Meters: "+pad_len_m
			
			pad_len_ft = float(pad_len_m)*3.048
			pad_width_ft = float(pad_width_m)*3.048
			
			pad_hdg = pad_len.get("azi2")
			
			pad_len_end = Geodesic.WGS84.Inverse(float(pad_lat_end), float(pad_lon_end), float(pad_lat), float(pad_lon))
			pad_hdg_end = str(360.0 + pad_len_end.get("azi2"))

			# Calculating runway points
			pad_direct_A = Geodesic.WGS84.Direct(float(pad_lat),float(pad_lon),float(pad_hdg-90.0),(float(pad_width_m))/2)
			A_lat = pad_direct_A.get("lat2")
			A_lon = pad_direct_A.get("lon2")
			
			pad_direct_B = Geodesic.WGS84.Direct(float(pad_lat),float(pad_lon),float(pad_hdg+90.0),(float(pad_width_m))/2)
			B_lat = pad_direct_B.get("lat2")
			B_lon = pad_direct_B.get("lon2")
			
			pad_direct_C = Geodesic.WGS84.Direct(float(pad_lat_end),float(pad_lon_end),-360.0 + float(pad_hdg_end)-90.0,(float(pad_width_m))/2)
			C_lat = pad_direct_C.get("lat2")
			C_lon = pad_direct_C.get("lon2")
			
			pad_direct_D = Geodesic.WGS84.Direct(float(pad_lat_end),float(pad_lon_end),-360.0 + float(pad_hdg_end)+90.0,(float(pad_width_m))/2)
			D_lat = pad_direct_D.get("lat2")
			D_lon = pad_direct_D.get("lon2")
			
			# Collecting runway points
			points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
			
			# We only collect for the heliports, there we need the points for the center, NOT for the airports
			if apt_name_ascii.startswith("[H]"):
				collecting(points, pad_len_m, pad_app_lighting)
			
			insert_helipad(apt_ident, pad_ident, pad_lon, pad_lat, pad_lon_end, pad_lat_end, pad_hdg, pad_hdg_end, pad_len_m, pad_len_ft, pad_width_m, pad_width_ft, pad_surface, pad_marking, pad_shoulder, pad_edge_lighting, pad_app_lighting, pad_xplane_code,\
			A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon)
			
		
		# ATC frequencies
		# Calculating range later ?
		# NM factor = 1.852
		# Standard range = 50 nm = 92,6 km
		
		if line.startswith("50 "):
			frq_type = "AWOS, ASOS or ATIS"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		if line.startswith("51 "):
			frq_type = "Unicom (US), CTAF (US), Radio (UK)"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		if line.startswith("52 "):
			frq_type = "Clearance Delivery"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		if line.startswith("53 "):
			frq_type = "Ground"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		if line.startswith("54 "):
			frq_type = "Tower"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		if line.startswith("55 "):
			frq_type = "Approach"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		if line.startswith("56 "):
			frq_type = "Departure"
			get_freqline(line)
			insert_freq(apt_ident, frq_type, frq_freq, frq_freq_nice, frq_description, frq_range_km, frq_range_nm, frq_xplane_code)
			
		# One green and two white flashes means military airport - no civil aircraft allowed.
		# xplane data beacon type code 4: military
		global bcn_type
		
		if line.startswith("18 "):
			bcn_type_read = line[31:32]
			bcn_type = str(bcn_type_read)
			
		# When there is a tower frequency, there are services probably
		global apt_services
		
		if line.startswith("54 "):
			apt_services = "1"
		else:
			apt_services = "0"
			
			
		global pointscollected
		global runwaycount
		global rwy_len_collect
		global apt_max_rwy_len_ft
		global apt_min_rwy_len_ft
		global apt_size
		global lightingcollected
		global apt_ifr
		global apt_center_lon
		global apt_center_lat
		global apt_authority
		global apt_country
		global apt_name_utf8
		global apt_local_code
			
		if line.startswith("\r\n"):
			# Now this is a new line, means a new airport
			
			#warnings.filterwarnings("ignore", category=SyntaxWarning)
			
			try:
				get_rwy_min_max(rwy_len_collect)
				get_ifr(lightingcollected)
				get_authority(bcn_type)
				insert_airport(apt_ident, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type)
				conn.commit()
				
			except:
				log.write("There is a suspicious line in apt.dat (probably wrong newline):\n")
				log.write("Identifier of last airport line scanned: "+apt_ident+"\n")
				pass
				
			pointscollected = ""
			runwaycount = 0
			rwy_len_collect = []
			apt_max_rwy_len_ft = 0
			apt_min_rwy_len_ft = 0
			apt_size = ""
			lightingcollected = []
			apt_ifr = "0"
			apt_center_lon = ""
			apt_center_lat = ""
			apt_authority = ""
			apt_services = ""
			apt_country = ""
			apt_name_utf8 = ""
			apt_local_code = ""
			bcn_type = ""
			
			

readxplane()

# The parser has some tolerance with wrong newlines, but we
# need to remove duplicates produced with tolerance.
# This is not that dangerous, because the apt_ident should
# be unique anyway ...

cur.execute("DELETE FROM airport WHERE apt_pk NOT IN (SELECT MAX(dup.apt_pk) FROM airport As dup GROUP BY dup.apt_ident);")
print "Removing duplicates ...\n"
log.write("Duplicates removed.\n")
conn.commit()

cur.close()
conn.close()


	
conn2 = psycopg2.connect(connectstring)
cur2 = conn2.cursor()

latsql = "SELECT * FROM airport;"

cur2.execute(latsql)
rows = cur2.fetchall()


for row in rows:
	latsql = "SELECT apt_center_lat84,apt_center_lon84 FROM airport WHERE apt_pk="+str(row[0])+";"
	#print latsql
	cur2.execute(latsql)
	
	
	
	conn2.commit()
	
	latlon = cur2.fetchall()[0]
	lat84 = latlon[0]
	lon84 = latlon[1]
	
	print lon84, lat84
	
	circles = drawcircle(18570,lon84,lat84)
	
	thiscirclenow = circles[:-2]+")"
	
	#print thiscirclenow

	# Wrapper function by Mike Toews from PostGIS forums, to NULL case projection failure
	# ... implemented, but not very useful
	#
	# CREATE OR REPLACE FUNCTION st_transform_null(geometry, integer)
	# RETURNS geometry AS
    # $BODY$BEGIN
    # RETURN st_transform($1, $2);
    # EXCEPTION WHEN internal_error THEN
    # RETURN NULL;
    # END;$BODY$
	# LANGUAGE 'plpgsql' IMMUTABLE STRICT
    # COST 100;
    #
	
	# 22.4823 114.204
	
	#testsql = "SELECT ST_GeometryFromText('"+thiscirclenow+"', 4326);"
	#outputsd = cur2.execute(testsql)
	
	#print str(outputsd)
	
	rangesql = "UPDATE airport SET apt_range=ST_Transform(ST_GeometryFromText('"+thiscirclenow+"', 4326),3857) WHERE apt_pk="+str(row[0])+";"
	print rangesql
	cur2.execute(rangesql)
	conn2.commit()

conn2.close()

endtime = time.asctime()
log.write("Finished: "+endtime+"\n")

log.close()
temp_sql.close()

