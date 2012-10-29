#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

import sys, csv, os, re, psycopg2, yaml

# geographiclib 1.24 by (c) Charles Karney
from geographiclib.geodesic import Geodesic

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python airport.py <file.dat>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python airport.py <file.dat>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]

conf = open('database.yaml')
confMap = yaml.load(conf)
conf.close()

fields = open('airport.yaml')
airportMap = yaml.load(fields)
fields.close()

connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']

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
	
# Collect runway points to insert airport center with ST_Centroid for all runway points,
# collect runway length to insert min/max runway length (feet)
def collecting(points, rwy_len, rwy_approach_lighting):
	global pointscollected
	pointscollected += points
	
	global runwaycount
	runwaycount += 1
	
	global rwy_len_collect
	rwy_len_collect.append(rwy_len)
	
	# Check if there is an approach light and indicate if IFR is available or not
	# Needs to be discussed this one
	global lightingcollected
	lightingcollected += rwy_approach_lighting


# Look for min/max runway length in rwy_len_collect
# prepared for a more sophisticated list type
def get_rwy_min_max(rwy_len_collect):

	how_many_large_rwy = 0
	
	lenlist = zip(rwy_len_collect)
	
	global apt_max_rwy_len_ft
	global apt_min_rwy_len_ft
	apt_max_rwy_len_ft = int(round(float(map(max, zip(*lenlist))[0])))
	apt_min_rwy_len_ft = int(round(float(map(min, zip(*lenlist))[0])))
	
	# Counting runways longer than 3500 meters
	for i in rwy_len_collect:
		if int(float(i)) >= 3500:
			how_many_large_rwy += 1
	
	# 3 runways >= 3500 meter = large
	# at least 1 runway >= 3500 meter = medium
	# rest = small
	global apt_size
	if how_many_large_rwy >= 3:
		apt_size = "large"
	elif how_many_large_rwy >= 1:
		apt_size = "medium"
	else:
		apt_size = "small"
		
def get_ifr(lightingcollected):
	for i in lightingcollected:
		if i != "0":
			global apt_ifr
			apt_ifr = "1"
			
def get_authority(bcn_type):
	global apt_authority
	if bcn_type == "4":
		apt_authority = "mil"
	else:
		apt_authority = "civ"
		
def insert_airport(apt_gps_code, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type):

	lastcoma = len(pointscollected)-1
	pointscollected2 = pointscollected[0:lastcoma] 
	
	apt_center = "MULTIPOINT ("+pointscollected2+")"
	
	apt_rwy_count = runwaycount
	
	# Geometry is reprojected to EPSG:3857, should become a command line parameter
	sql = '''
		INSERT INTO airport (apt_gps_code, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type, apt_rwy_count, apt_min_rwy_len_ft, apt_max_rwy_len_ft, apt_size, apt_xplane_code, apt_ifr, apt_authority, apt_services, apt_center)
		VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_Centroid(ST_Transform(ST_GeomFromText(%s, 4326),3857)))'''
		
	#print sql
	
	params = [apt_gps_code, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type, apt_rwy_count, apt_min_rwy_len_ft, apt_max_rwy_len_ft, apt_size, apt_xplane_code, apt_ifr, apt_authority, apt_services, apt_center]
	cur.execute(sql, params)
	
	# Now this second query gives lon/lat (postgis x/y) as text for the center point
	sql2 = "UPDATE airport SET apt_center_lon=ST_X(apt_center), apt_center_lat=ST_Y(apt_center) WHERE apt_gps_code='"+apt_gps_code+"';"
	cur.execute(sql2)
				

def readxplane():
	reader = open(inputfile, 'r')
	
	for line in reader:
	
		# airport line
		if line.startswith("1  "):
		
			apt_xplane_code_read = line[0]+line[1]
			apt_elev_ft_read = line[5]+line[6]+line[7]+line[8]+line[9]
			apt_deprecated1 = line[11]
			apt_deprecated2 = line[13]
			apt_gps_code_read = line[15]+line[16]+line[17]+line[18]
			
			tilend = len(line)
			apt_name_ascii_read = line[20:tilend-2]
						
			global apt_gps_code
			apt_gps_code = apt_gps_code_read
			global apt_name_ascii
			apt_name_ascii = apt_name_ascii_read
			global apt_elev_ft
			apt_elev_ft = apt_elev_ft_read
			global apt_elev_m
			apt_elev_m = int(float(apt_elev_ft_read)*0.3048)
			global apt_type
			apt_type = "land"
			global apt_xplane_code
			apt_xplane_code = apt_xplane_code_read
			
			print "--- Processing airport:" + apt_gps_code
		
		# runways
		if line.startswith("100 "):
		
			rwy_id = str(line[31:34])
			rwy_id_end = str(line[87:90])
		
			rwy_linecode = line[0:3]
			rwy_width =  line[5:13]
			rwy_surface = line[14:16].replace(" ","")
			rwy_shoulder = line[17:19].replace(" ","")
			rwy_smoothness = line[20:24]
			rwy_centerline_lights = line[25]
			rwy_edge_lighting = line[27]
			rwy_autogenerate_distance_signs = line[29]
			rwy_number = str(line[31:34])
			rwy_lat = line[34:47]
			rwy_lon = line[48:61]
			rwy_threshold = line[62:69]
			rwy_overrun = line[70:77]
			rwy_marking = line[78:79]
			rwy_approach_lighting = line[81:82]
			rwy_touchdown_zone_lighting = line[83]
			rwy_reil = line[85]
			rwy_number_end = str(line[87:90])
			rwy_lat_end = line[90:103]
			rwy_lon_end = line[104:117]
			rwy_threshold_end = line[119:125]
			rwy_overrun_end = line[126:133]
			rwy_marking_end = line[134:135]
			rwy_approach_lighting_end = line[136:138].replace(" ","")
			rwy_touchdown_zone_lighting_end = line[139]
			rwy_reil_end = line[141]
			
			# Now some additional data, not in apt.dat
			
			rwy_length = Geodesic.WGS84.Inverse(float(rwy_lat), float(rwy_lon), float(rwy_lat_end), float(rwy_lon_end))
			rwy_length_meters = str(rwy_length.get("s12"))
			
			rwy_length_feet = rwy_length.get("s12")*3.048
			
			rwy_heading = rwy_length.get("azi2")
			
			rwy_length_end = Geodesic.WGS84.Inverse(float(rwy_lat_end), float(rwy_lon_end), float(rwy_lat), float(rwy_lon))
			rwy_heading_end = str(360.0 + rwy_length_end.get("azi2"))
			
			rwy_threshold_direct = Geodesic.WGS84.Direct(float(rwy_lat),float(rwy_lon),float(rwy_heading),float(rwy_threshold))
			rwy_threshold_direct_end = Geodesic.WGS84.Direct(float(rwy_lat_end),float(rwy_lon_end),rwy_length_end.get("azi2"),float(rwy_threshold_end))

			# Calculating runway points
			rwy_direct_A = Geodesic.WGS84.Direct(float(rwy_lat),float(rwy_lon),float(rwy_heading-90.0),(float(rwy_width))/2)
			A_lat = rwy_direct_A.get("lat2")
			A_lon = rwy_direct_A.get("lon2")
			
			rwy_direct_B = Geodesic.WGS84.Direct(float(rwy_lat),float(rwy_lon),float(rwy_heading+90.0),(float(rwy_width))/2)
			B_lat = rwy_direct_B.get("lat2")
			B_lon = rwy_direct_B.get("lon2")
			
			rwy_direct_C = Geodesic.WGS84.Direct(float(rwy_lat_end),float(rwy_lon_end),-360.0 + float(rwy_heading_end)-90.0,(float(rwy_width))/2)
			C_lat = rwy_direct_C.get("lat2")
			C_lon = rwy_direct_C.get("lon2")
			
			rwy_direct_D = Geodesic.WGS84.Direct(float(rwy_lat_end),float(rwy_lon_end),-360.0 + float(rwy_heading_end)+90.0,(float(rwy_width))/2)
			D_lat = rwy_direct_D.get("lat2")
			D_lon = rwy_direct_D.get("lon2")
			
			# Collecting runway points
			points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
			collecting(points, rwy_length_meters, rwy_approach_lighting)
			
			

			#print "Airport: "+apt_gps_code+ " " + "Runway: " + rwy_id + ", " + rwy_id_end
			
		# One green and two white flashes means military airport - no civil aircraft allowed.
		# xplane data beacon type code 4: military
		if line.startswith("18 "):
			bcn_type_read = line[31:32]
			global bcn_type
			bcn_type = str(bcn_type_read)
			
		# When there is a tower frequency, there are services probably
		if line.startswith("54 "):
			global apt_services
			apt_services = "1"
			
			

readxplane()

get_rwy_min_max(rwy_len_collect)

get_ifr(lightingcollected)

get_authority(bcn_type)

insert_airport(apt_gps_code, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type)

conn.commit()
cur.close()
conn.close()

print "--- "+apt_gps_code+" xplane-data imported."

# Now take data from ourairports for various fields, if available

def readourairports():
	reader = open("../../data/ourairports/airports.csv", 'r')
	csvreader = csv.reader(reader)
	
	conn = psycopg2.connect(connectstring)
	cur = conn.cursor()

	for row in csvreader:
		if row[1] == apt_gps_code:
			global apt_local_code
			apt_local_code = row[13]
			global apt_country
			apt_country = row[8]
			global apt_name_utf8
			apt_name_utf8 = row[3]
			
			sql3 = "UPDATE airport SET apt_country='"+apt_country+"', apt_local_code='"+apt_local_code+"', apt_name_utf8='"+apt_name_utf8+"' WHERE apt_gps_code='"+row[1]+"';"
			cur.execute(sql3)
	conn.commit()
	cur.close()
	conn.close()
	
	print "--- Updated '"+apt_name_utf8+"' with ourairports data."
	print "--- SUCCESS"
		
readourairports()

