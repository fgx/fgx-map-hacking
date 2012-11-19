#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#



import sys, time, datetime, csv, os, re #, psycopg2, yaml, warnings
import fileinput

# geographiclib 1.24 by (c) Charles Karney
from geographiclib.geodesic import Geodesic

from geoalchemy import WKTSpatialElement
from sqlalchemy.sql.expression import func 

from fgx.model import meta, Airport, FGX_SRID


class Attr:
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
def collecting(A, points, rwy_len, rwy_approach_lighting):

	A.pointscollected += points

	A.runwaycount += 1

	A.rwy_len_collect.append(rwy_len)

	# Check if there is an approach light and indicate if IFR is available or not
	# Needs to be discussed this one
	A.lightingcollected += rwy_approach_lighting


# Look for min/max runway length in rwy_len_collect
# prepared for a more sophisticated list type
def get_rwy_min_max(A):

	how_many_large_rwy = 0

	lenlist = zip(A.rwy_len_collect)

	A.apt_max_rwy_len_ft = int(round(float(map(max, zip(*lenlist))[0])*3.048))
	A.apt_min_rwy_len_ft = int(round(float(map(min, zip(*lenlist))[0])*3.048))

	# Counting runways longer than 3200 meters / 9700 feet
	for i in A.rwy_len_collect:
		if int(float(i) * 3.048) >= 9700:
			how_many_large_rwy += 1

	# 2 runways >= 3200 meter = large
	# at least 1 runway >= 3200 meter = medium
	# rest = small
	# @ pete also if its ILS then its not small
	#global apt_size
	if how_many_large_rwy >= 2:
		apt_size = "large"
		
	elif how_many_large_rwy >= 1:
		apt_size = "medium"
		
	else:
		apt_size = "small"

def get_ifr(A):
	A.apt_ifr = 0
	for i in A.lightingcollected:
		if i != "0":
			A.apt_ifr = 1

			
def get_authority(A, apt_name_ascii):
	
	if A.bcn_type == "4":
		A.apt_authority = "mil"
	else:
		if apt_name_ascii.startswith("[X]"):
			A.apt_authority = "clo"
		else:
			A.apt_authority = "civ"
			
			

def insert_airport(A, apt_identifier, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type):

	lastcoma = len(A.pointscollected)-1
	pointscollected2 = A.pointscollected[0:lastcoma] 

	apt_center = "MULTIPOINT ("+ pointscollected2 +")"

	apt_rwy_count = A.runwaycount

	# Geometry is reprojected to EPSG:3857, should become a command line parameter
	
	## Create new DB object and insert
	ob = Airport()
	ob.apt_ident = apt_identifier
	ob.apt_name = apt_name_ascii
	ob.apt_elev_ft = apt_elev_ft
	ob.apt_elev_m = apt_elev_m
	ob.apt_type = apt_type
	ob.apt_rwy_count = apt_rwy_count
	ob.apt_min_rwy_len_ft = A.apt_min_rwy_len_ft
	ob.apt_max_rwy_len_ft = A.apt_max_rwy_len_ft
	ob.apt_size = A.apt_size
	#ob.apt_xplane_code = apt_xplane_code # TODO
	ob.apt_ifr = A.apt_ifr
	ob.apt_authority = A.apt_authority
	ob.apt_center = func.ST_GeomFromText(apt_center, FGX_SRID)
	meta.Session.add(ob)
	meta.Session.commit()
	

	# Now this second query gives lon/lat (postgis x/y) as text for the center point
	sql2 = "UPDATE airport SET apt_center_lon=ST_X(apt_center), apt_center_lat=ST_Y(apt_center) WHERE apt_ident = '%s';" %  ob.apt_ident
	#meta.Session.execute(sql2) # TODO


def import_dat(file_path, dev_mode=None, empty=None, verbose=None):
	
	#reader = fileinput.input(file_path)


	print "Processing: %s"  % file_path

	## Create a new attributes helper
	A = Attr()
	
	c = 0
	for raw_line in fileinput.input(file_path):
		
		c += 1
		if c <= 4:
			## Skip first three lines
			pass
		
		else:
			#print "=", raw_line
			line = raw_line.strip()
			
			# airport line
			if line.startswith("1  "):

				apt_xplane_code_read = line[0]+line[1]
				apt_elev_ft_read = line[5]+line[6]+line[7]+line[8]+line[9]
				apt_deprecated1 = line[11]
				apt_deprecated2 = line[13]
				apt_identifier_read = line[15]+line[16]+line[17]+line[18]

				tilend = len(line)
				apt_name_ascii_read = line[20:tilend-2]

				apt_identifier = apt_identifier_read
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
				apt_identifier_read = line[15]+line[16]+line[17]+line[18]

				tilend = len(line)
				apt_name_ascii_read = line[20:tilend-2]

				apt_identifier = apt_identifier_read
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
				apt_identifier_read = line[15]+line[16]+line[17]+line[18]

				tilend = len(line)
				apt_name_ascii_read = line[20:tilend-2]

				apt_identifier = apt_identifier_read
				apt_name_ascii = apt_name_ascii_read
				apt_elev_ft = apt_elev_ft_read
				apt_elev_m = int(float(apt_elev_ft_read)*0.3048)
				apt_type = "heli"
				apt_xplane_code = apt_xplane_code_read

			# runways, we need it for some calculation, i.e. centerpoint
			# but also for getting shortest/longest runway, to set the apt_ifr
			# flag and much more
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

				# The NZSP problem
				if apt_identifier == "NZSP":
						if rwy_lat_end > -90.0:
								rwy_lat_end = ( float(rwy_lat_end) + 90.0 )*-1.0
								log.write("NZSP problem solved in airport "+apt_identifier+", runway "+rwy_number+"\n")
						if rwy_lat > -90.0:
								rwy_lat = ( float(rwy_lat) + 90.0 )*-1.0
								log.write("NZSP problem solved in airport "+apt_identifier+", runway "+rwy_number+"\n")

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
				collecting(A, points, rwy_length_meters, rwy_approach_lighting)


			# WATER runways, we need it for some calculation, i.e. centerpoint
			if line.startswith("101 "):

					wwy_linecode = line[0:3]
					wwy_width =  line[4:11]
					wwy_buoys = line[12:13]
					wwy_id = str(line[14:16])
					wwy_lat = line[17:31]
					wwy_lon = line[32:45]

					wwy_id_end = str(line[46:48])
					wwy_lat_end = line[49:62]
					wwy_lon_end = line[63:79]

					wwy_approach_lighting = "0"

					# Now some additional data, not in apt.dat

					wwy_length = Geodesic.WGS84.Inverse(float(wwy_lat), float(wwy_lon), float(wwy_lat_end), float(wwy_lon_end))
					wwy_length_meters = str(wwy_length.get("s12"))

					#print "Meters: "+wwy_length_meters

					wwy_length_feet = wwy_length.get("s12")*3.048

					wwy_heading = wwy_length.get("azi2")

					wwy_length_end = Geodesic.WGS84.Inverse(float(wwy_lat_end), float(wwy_lon_end), float(wwy_lat), float(wwy_lon))
					wwy_heading_end = str(360.0 + wwy_length_end.get("azi2"))

					# Calculating runway points
					wwy_direct_A = Geodesic.WGS84.Direct(float(wwy_lat),float(wwy_lon),float(wwy_heading-90.0),(float(wwy_width))/2)
					A_lat = wwy_direct_A.get("lat2")
					A_lon = wwy_direct_A.get("lon2")

					wwy_direct_B = Geodesic.WGS84.Direct(float(wwy_lat),float(wwy_lon),float(wwy_heading+90.0),(float(wwy_width))/2)
					B_lat = wwy_direct_B.get("lat2")
					B_lon = wwy_direct_B.get("lon2")

					wwy_direct_C = Geodesic.WGS84.Direct(float(wwy_lat_end),float(wwy_lon_end),-360.0 + float(wwy_heading_end)-90.0,(float(wwy_width))/2)
					C_lat = wwy_direct_C.get("lat2")
					C_lon = wwy_direct_C.get("lon2")

					wwy_direct_D = Geodesic.WGS84.Direct(float(wwy_lat_end),float(wwy_lon_end),-360.0 + float(wwy_heading_end)+90.0,(float(wwy_width))/2)
					D_lat = wwy_direct_D.get("lat2")
					D_lon = wwy_direct_D.get("lon2")

					# Collecting runway points
					points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
					collecting(A, points, wwy_length_meters, wwy_approach_lighting)

			# HELIPADS, we need it for heliport calculation, i.e. centerpoint
			# but we dont want to take this points into account for regular airports
			# so we look out for (H)
			if line.startswith("102 ") and apt_name_ascii.startswith("[H]"):

					pad_linecode = line[0:3]
					pad_id = str(line[4:6])
					pad_lat_read = line[7:19]
					pad_lon_read = line[21:33]
					pad_heading_tr = line[34:41]
					pad_length_m = line[42:49]
					pad_width_m = line[50:57]
					pad_surface = line[58:61]
					pad_marking = line[61:63]
					pad_shoulder = line[65:67]
					pad_smoothness = line[68:72]
					pad_edgelighting = line[73]

					pad_approach_lighting = "0"

					# Now some additional data, not in apt.dat

					# We get the centerpoint of the pad, but we want the center point at shape start, 
					# to get it calculated like runways and to prevent me from writing all separated for pads
					pad_direct = Geodesic.WGS84.Direct(float(pad_lat_read),float(pad_lon_read),float(pad_heading_tr)-180.0,(float(pad_length_m))/2)
					pad_lat = pad_direct.get("lat2")
					pad_lon = pad_direct.get("lon2")

					pad_direct_end = Geodesic.WGS84.Direct(float(pad_lat_read),float(pad_lon_read),float(pad_heading_tr),(float(pad_length_m)))
					pad_lat_end = pad_direct_end.get("lat2")
					pad_lon_end = pad_direct_end.get("lon2")

					pad_length = Geodesic.WGS84.Inverse(float(pad_lat), float(pad_lon), float(pad_lat_end), float(pad_lon_end))
					pad_length_meters = str(pad_length.get("s12"))

					print "Meters: "+pad_length_m

					pad_length_ft = float(pad_length_m)*3.048

					pad_heading = pad_length.get("azi2")

					pad_length_end = Geodesic.WGS84.Inverse(float(pad_lat_end), float(pad_lon_end), float(pad_lat), float(pad_lon))
					pad_heading_end = str(360.0 + pad_length_end.get("azi2"))

					# Calculating runway points
					pad_direct_A = Geodesic.WGS84.Direct(float(pad_lat),float(pad_lon),float(pad_heading-90.0),(float(pad_width_m))/2)
					A_lat = pad_direct_A.get("lat2")
					A_lon = pad_direct_A.get("lon2")

					pad_direct_B = Geodesic.WGS84.Direct(float(pad_lat),float(pad_lon),float(pad_heading+90.0),(float(pad_width_m))/2)
					B_lat = pad_direct_B.get("lat2")
					B_lon = pad_direct_B.get("lon2")

					pad_direct_C = Geodesic.WGS84.Direct(float(pad_lat_end),float(pad_lon_end),-360.0 + float(pad_heading_end)-90.0,(float(pad_width_m))/2)
					C_lat = pad_direct_C.get("lat2")
					C_lon = pad_direct_C.get("lon2")

					pad_direct_D = Geodesic.WGS84.Direct(float(pad_lat_end),float(pad_lon_end),-360.0 + float(pad_heading_end)+90.0,(float(pad_width_m))/2)
					D_lat = pad_direct_D.get("lat2")
					D_lon = pad_direct_D.get("lon2")

					# Collecting runway points
					points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","
					collecting(points, pad_length_meters, pad_approach_lighting)


			# One green and two white flashes means military airport - no civil aircraft allowed.
			# xplane data beacon type code 4: military
			if line.startswith("18 "):
				bcn_type_read = line[31:32]
				bcn_type = str(bcn_type_read)

			# When there is a tower frequency, there are services probably
			if line.startswith("54 "):
				apt_services = 1
			else:
				apt_services = 0


			if line == "":
				# Now this is a new line, means commit last before  a new airport

				#try:
				get_rwy_min_max(A)
				get_ifr(A)
				get_authority(A, apt_name_ascii)
				insert_airport(A, apt_identifier, apt_name_ascii, apt_elev_ft, apt_elev_m, apt_type)


				#except:
				#		log.write("There is a suspicious line in apt.dat (probably wrong newline):\n")
				#		log.write("Identifier of last airport line scanned: "+apt_identifier+"\n")
				#		pass
				A = Attr()

