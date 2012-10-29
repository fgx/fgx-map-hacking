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

pointscollected = ""

conn = psycopg2.connect(connectstring)
cur = conn.cursor()
	
# Collect runway points to insert Airport with ST_Centroid
def collectpoints(points):
	global pointscollected
	pointscollected += points


def insert_airport(apt_gps_code, apt_name_ascii, apt_elev_ft):

	lastcoma = len(pointscollected)-1
	pointscollected2 = pointscollected[0:lastcoma] 
	
	apt_geometry = "MULTIPOINT ("+pointscollected2+")"
	#print apt_geometry
	
	# Geometry is reprojected to EPSG:3857
	sql = '''
		INSERT INTO airport (apt_gps_code, apt_name_ascii, apt_elev_ft, apt_center)
		VALUES (%s, %s, %s, ST_Centroid(ST_Transform(ST_GeomFromText(%s, 4326),3857)))'''
		
	#print sql
	
	params = [apt_gps_code, apt_name_ascii, apt_elev_ft, apt_geometry]
	cur.execute(sql, params)
				

def readapt():
	reader = open(inputfile, 'r')
	
	for line in reader:
	
		# airport line
		if line.startswith("1  "):
		
			apt_xplane_code = line[0]+line[1]
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
			
			print "Processing airport:" + apt_gps_code
		
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
			collectpoints(points)

			#print "Airport: "+apt_gps_code+ " " + "Runway: " + rwy_id + ", " + rwy_id_end

readapt()

insert_airport(apt_gps_code, apt_name_ascii, apt_elev_ft)

conn.commit()
cur.close()
conn.close()

print "--- SUCESS ---"

