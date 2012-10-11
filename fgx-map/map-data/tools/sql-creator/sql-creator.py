#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#


import sys, csv, os, re, psycopg2
from xml.dom.minidom import Document

# geographiclib 1.24 by (c) Charles Karney
from geographiclib.geodesic import Geodesic

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python sql-creator.py <file.dat>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python sql-creator.py <file.dat>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]

apt = Document()

pointscollected = ""

conn = psycopg2.connect("dbname=xplanedata1000 user=user password=password")
cur = conn.cursor()
#cur.execute("DROP TABLE IF EXISTS runways;")
#cur.execute("CREATE TABLE runways (ogc_fid serial PRIMARY KEY, \
#			icao varchar, \
#			rwy_id varchar, \
#			rwy_id_end varchar, \
#			rwy_width varchar, \
#			rwy_length_meters varchar, \
#			rwy_length_feet varchar, \
#			wkb_geometry geometry(Polygon,3857));")
			
#cur.execute("DROP TABLE IF EXISTS airports;")
#cur.execute("CREATE TABLE airports (ogc_fid serial PRIMARY KEY, \
#			icao varchar, \
#			name varchar, \
#			elevation varchar, \
#			wkb_geometry geometry(Point,3857));")


propertylist = apt.createElement("PropertyList")
apt.appendChild(propertylist)

airport = apt.createElement("airport")
propertylist.appendChild(airport)


def insert_runway(ap_identifier,\
				rwy_id,\
				rwy_id_end,\
				rwy_width,\
				rwy_lon,\
				rwy_lat,\
				rwy_lon_end,\
				rwy_lat_end,\
				rwy_length_feet,\
				rwy_length_meters,\
				rwy_heading,\
				rwy_heading_end, \
				A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon):
				
	# Coordinate ordering is (x, y) -- that is (lon, lat)
	# Polygon needs to be closed, repeating starting point
	rwy_polygon = "POLYGON (( " + str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + "," + str(A_lon) + " " + str(A_lat) + " ))"
	#print rwy_polygon
	
	# Geometry is reprojected to EPSG:3857
	sql = '''
		INSERT INTO runways (icao, rwy_id, rwy_id_end, rwy_width, rwy_length_meters, rwy_length_feet, wkb_geometry)
		VALUES (%s, %s, %s, %s, %s, %s, ST_Transform(ST_GeomFromText(%s, 4326),3857))'''
	params = [ap_identifier, rwy_id, rwy_id_end, rwy_width, rwy_length_meters, rwy_length_feet, rwy_polygon]
	cur.execute(sql, params)
	
	points = str(A_lon) + " " + str(A_lat) + "," + str(B_lon) + " " + str(B_lat) + "," + str(C_lon) + " " + str(C_lat) + "," + str(D_lon) + " " + str(D_lat) + ","

	collectpoints(points)
	
# Collect runway points to insert Airport with ST_Centroid
def collectpoints(points):
	global pointscollected
	pointscollected += points
	#print pointscollected
	

def insert_airport(ap_identifier, ap_name, ap_elevation):

	lastcoma = len(pointscollected)-1
	pointscollected2 = pointscollected[0:lastcoma] 
	
	ap_geometry = "MULTIPOINT ("+pointscollected2+")"
	print ap_geometry
	
	# Geometry is reprojected to EPSG:3857
	sql = '''
		INSERT INTO airports (icao, name, elevation, wkb_geometry)
		VALUES (%s, %s, %s, ST_Centroid(ST_Transform(ST_GeomFromText(%s, 4326),3857)))'''
		
	#print sql
	
	params = [ap_identifier, ap_name, ap_elevation, ap_geometry]
	cur.execute(sql, params)
	 


def generate_node(parent,node_name,node_value,space_replace):

	node_value_clean = ""

	if space_replace == 1:
		node_value_clean = node_value.replace(" ","")
		
	else:
		node_value_clean = node_value
		
	gen_name = apt.createElement(node_name)
	parent.appendChild(gen_name)
	gen_valuetext = apt.createTextNode(node_value_clean)
	gen_name.appendChild(gen_valuetext)
	
def generate_node_with_attribute(parent,node_name,node_value,attribute_name,attribute_value,space_replace):

	node_value_clean = ""

	if space_replace == 1:
		node_value_clean = node_value.replace(" ","")
		attribute_value_clean = attribute_value.replace(" ","")
		
	else:
		node_value_clean = node_value
		attribute_value_clean = attribute_value
		
	gen_name = apt.createElement(node_name)
	gen_name.setAttribute(attribute_name,attribute_value)
	parent.appendChild(gen_name)
	gen_valuetext = apt.createTextNode(node_value_clean)
	gen_name.appendChild(gen_valuetext)
		

def getsurface(code):
	surfaces = {'1':'Asphalt', 
				'2':'Concrete', 
				'3':'Turf or Grass', 
				'4':'Dirt (brown)', 
				'5':'Gravel (grey)', 
				'12':'Dry lakebed', 
				'13':'Water', 
				'14':'Snow or Ice', 
				'15':'Transparent'}
	return surfaces.get(code)
	
	
def getshoulder(code):
	shoulders = {'0':'No shoulder',
				 '1':'Asphalt shoulder',
				 '2':'Concrete shoulder'}
	return shoulders.get(code)
	
def getcenterlinelights(code):
	centerlinelights = {'0':'No centerline lights',
				 '1':'Centerline lights'}
	return centerlinelights.get(code)
	
def getedgelights(code):
	edgelights = {'0':'No edge lights',
				 '1':'Edge lights',
				 '2':'Medium intensity edge lights'}
	return edgelights.get(code)
	
def getrunwaymarking(code):
	runwaymarkings = {
				'0':'No runway markings', 
				'1':'Visual markings', 
				'2':'Non precision approach markings', 
				'3':'Presicision approach markings', 
				'4':'UK-style non-precision approach markings', 
				'5':'UK-style precision approach markings'}
	return runwaymarkings.get(code)
	
def getapproachlighting(code):
	approachlightings = {
				'0':'No approach lighting',
				'1':'ALSF-I',
				'2':'ALSF-II',
				'3':'Calvert',
				'4':'Calvert ILS Cat II and Cat II',
				'5':'SSALR',
				'6':'SSALF',
				'7':'SALS',
				'8':'MALSR',
				'9':'MALSF',
				'10':'MALS',
				'11':'ODALS',
				'12':'RAIL'}
	return approachlightings.get(code)
	
def getreil(code):
	reillightings = {
				'0':'No REIL',
				'1':'omni-directional REIL',
				'2':'unidirectional REIL'}
	return reillightings.get(code)
	
def gethelipadsurface(code):
	helipadsurfaces = {'1':'Asphalt', 
				'2':'Concrete', 
				'3':'Turf or Grass', 
				'4':'Dirt (brown)', 
				'5':'Gravel (grey)', 
				'12':'Dry lakebed', 
				'13':'Water', 
				'14':'Snow or Ice', 
				'15':'Transparent'}
	return helipadsurfaces.get(code)
	
def gethelipadmarking(code):
	helipadmarkings = {
				'0':'Not supported yet'}
	return helipadmarkings.get(code)
	
def gethelipadshouldersurface(code):
	helipadshouldersurfaces = {
				'0':'No shoulder',
				'1':'Asphalt shoulder',
				'2':'Concrete shoulder'}
	return helipadshouldersurfaces.get(code)
	
def gethelipadedgelighting(code):
	helipadedgelightings = {
				'0':'No edge lights',
				'1':'Yellow edge lights'}
	return helipadedgelightings.get(code)
	
def getlightbeacontype(code):
	lightbeacontypes = {
				'0':'No beacon (suppress autp-generation)',
				'1':'White-green flashing',
				'2':'White-yellow flashing',
				'3':'Green-yellow-white flashing',
				'4':'White-white-green flashing'}
	return lightbeacontypes.get(code)
	
def getwindsocklighting(code):
	windsocklightings = {
				'0':'Unlit',
				'1':'Illuminated'}
	return windsocklightings.get(code)
	
def getsignsize(code):
	signsizes = {
				'1':'Small taxiway sign',
				'2':'Medium taxiway sign',
				'3':'Large taxiway sign',
				'4':'Large distance-remaining sign on runway edge',
 				'5':'Small distance-remaining sign on runway edge'}
 	return signsizes.get(code)
 	
def getlightingobjecttype(code):
 	lightingobjecttypes = {
 				'1':'VASI Location is centre point between the two VASI units',
  				'2':'PAPI-4L (four-light) on left of runway',
  				'3':'PAPI-4R (four light) on right of runway',
  				'4':'Space Shuttle PAPI, 20 degree glidepath',
  				'5':'Tri-colour VASI',
  				'6':'Runway guard (wig-wag) lights'}
  	return lightingobjecttypes.get(code)
				

def readapt():
	reader = open(inputfile, 'r')
	
	for line in reader:
	
		# airport line
		if line.startswith("1  "):
		
			ap_linecode = line[0]+line[1]
			#generate_node(airport,"linecode",ap_linecode,1)
			
			ap_elevation = line[5]+line[6]+line[7]+line[8]+line[9]
			#generate_node(airport,"elevation",ap_elevation,1)
			
			ap_deprecated1 = line[11]
			#generate_node(airport,"deprecated1",ap_deprecated1,0)
			
			ap_deprecated2 = line[13]
			#generate_node(airport,"deprecated2",ap_deprecated2,0)
			
			ap_identifier = line[15]+line[16]+line[17]+line[18]
			#generate_node(airport,"identifier",ap_identifier,1)
			
			tilend = len(line)
			ap_name = line[20:tilend-2]
			#generate_node(airport,"name",ap_name,0)
			
			#airport.setAttribute("id",ap_identifier)
			
			global ap_identifier_ins
			global ap_name_ins
			global ap_elevation_ins
			
			ap_identifier_ins = ap_identifier
			ap_name_ins = ap_name
			ap_elevation_ins = ap_elevation
		
		# runways
		if line.startswith("100 "):
		
			runway = apt.createElement("runway")
			rw_id = str(line[31:34])
			rw_id_end = str(line[87:90])
			runway.setAttribute("id", rw_id.replace(" ",""))
			runway.setAttribute("end", rw_id_end.replace(" ",""))
			airport.appendChild(runway)
		
			rw_linecode = line[0:3]
			#generate_node(runway,"linecode",rw_linecode,1)
			
			rw_width =  line[5:13]
			#generate_node(runway,"width",rw_width,1)
			
			rw_surface = line[14:16].replace(" ","")
			#generate_node_with_attribute(runway,"surface",getsurface(rw_surface),"code",rw_surface,0)
			
			rw_shoulder = line[17:19].replace(" ","")
			#generate_node_with_attribute(runway,"shoulder",str(getshoulder(rw_shoulder)),"code",rw_shoulder,0)
			
			rw_smoothness = line[20:24]
			#generate_node(runway,"smoothness",rw_smoothness,1)
			
			rw_centerline_lights = line[25]
			#generate_node_with_attribute(runway,"centerline_lights",str(getcenterlinelights(rw_centerline_lights)),"code",rw_centerline_lights,0)
			
			rw_edge_lighting = line[27]
			#generate_node_with_attribute(runway,"edge_lighting",str(getedgelights(rw_edge_lighting)),"code",rw_edge_lighting,0)
			
			rw_autogenerate_distance_signs = line[29]
			#generate_node(runway,"autogenerate_distance_signs",rw_autogenerate_distance_signs,0)
			
			rw_number = str(line[31:34])
			#generate_node(runway,"number",rw_number,1)
			
			rw_lat = line[34:47]
			#generate_node(runway,"latitude",rw_lat,1)
			
			rw_lon = line[48:61]
			#generate_node(runway,"longitude",rw_lon,1)
			
			rw_threshold = line[62:69]
			#generate_node(runway,"threshold",rw_threshold,1)
			
			rw_overrun = line[70:77]
			#generate_node(runway,"overrrun",rw_overrun,1)
			
			rw_marking = line[78:79]
			#generate_node_with_attribute(runway,"marking",str(getrunwaymarking(rw_marking)),"code",rw_marking,0)
			
			rw_approach_lighting = line[81:82]
			#generate_node_with_attribute(runway,"approach_lighting",str(getapproachlighting(rw_approach_lighting)),"code",rw_approach_lighting,0)
			
			rw_touchdown_zone_lighting = line[83]
			#generate_node(runway,"touchdown_zone_lighting",rw_touchdown_zone_lighting,1)
			
			rw_reil = line[85]
			#generate_node_with_attribute(runway,"reil",str(getreil(rw_reil)),"code",rw_reil,0)
			
			rw_number_end = str(line[87:90])
			#generate_node(runway,"number_end",rw_number_end,1)
			
			rw_lat_end = line[90:103]
			#generate_node(runway,"latitude_end",rw_lat_end,1)
			
			rw_lon_end = line[104:117]
			#generate_node(runway,"longitude_end",rw_lon_end,1)
			
			rw_threshold_end = line[119:125]
			#generate_node(runway,"threshold_end",rw_threshold_end,1)
			
			rw_overrun_end = line[126:133]
			#generate_node(runway,"overrrun_end",rw_overrun_end,1)
			
			rw_marking_end = line[134:135]
			#generate_node_with_attribute(runway,"marking_end",str(getrunwaymarking(rw_marking_end)),"code",rw_marking_end,0)
			
			rw_approach_lighting_end = line[136:138].replace(" ","")
			#generate_node_with_attribute(runway,"approach_lighting_end",str(getapproachlighting(rw_approach_lighting_end)),"code",rw_approach_lighting_end,0)
			
			rw_touchdown_zone_lighting_end = line[139]
			#generate_node(runway,"touchdown_zone_lighting_end",rw_touchdown_zone_lighting_end,1)
			
			rw_reil_end = line[141]
			#generate_node_with_attribute(runway,"reil_end",str(getreil(rw_reil_end)),"code",rw_reil_end,0)
			
			# Now some additional data, not in apt.dat
			
			spacer_above = apt.createComment("++++++++++++++++++++++++++++++")
			comment = apt.createComment("Additonal data, not in apt.dat")
			spacer_below = apt.createComment("++++++++++++++++++++++++++++++")
			runway.appendChild(spacer_above)
			runway.appendChild(comment)
			runway.appendChild(spacer_below)
			
			rw_length = Geodesic.WGS84.Inverse(float(rw_lat), float(rw_lon), float(rw_lat_end), float(rw_lon_end))
			rw_length_meters = str(rw_length.get("s12"))
			#generate_node(runway,"length-meters",str(rw_length.get("s12")),0)
			
			rw_length_feet = rw_length.get("s12")*3.048
			#generate_node(runway,"length-feet",str(rw_length_feet),0)
			
			rw_heading = rw_length.get("azi2")
			#generate_node_with_attribute(runway,"heading",str(rw_heading),"id",rw_number,0)
			
			rw_length_end = Geodesic.WGS84.Inverse(float(rw_lat_end), float(rw_lon_end), float(rw_lat), float(rw_lon))
			rw_heading_end = str(360.0 + rw_length_end.get("azi2"))
			#generate_node_with_attribute(runway,"heading_end",str(360.0 + rw_length_end.get("azi2")),"id",rw_number_end,0)
			
			rw_threshold_direct = Geodesic.WGS84.Direct(float(rw_lat),float(rw_lon),float(rw_heading),float(rw_threshold))
			rw_threshold_direct_end = Geodesic.WGS84.Direct(float(rw_lat_end),float(rw_lon_end),rw_length_end.get("azi2"),float(rw_threshold_end))
			#generate_node_with_attribute(runway,"threshold_lat",str(rw_threshold_direct.get("lat2")),"id",rw_number,0)
			#generate_node_with_attribute(runway,"threshold_lon",str(rw_threshold_direct.get("lon2")),"id",rw_number,0)
			#generate_node_with_attribute(runway,"threshold_lat_end",str(rw_threshold_direct_end.get("lat2")),"id",rw_number_end,0)
			#generate_node_with_attribute(runway,"threshold_lon_end",str(rw_threshold_direct_end.get("lon2")),"id",rw_number_end,0)
			
			
			rw_direct_A = Geodesic.WGS84.Direct(float(rw_lat),float(rw_lon),float(rw_heading-90.0),(float(rw_width))/2)
			A_lat = rw_direct_A.get("lat2")
			A_lon = rw_direct_A.get("lon2")
			
			rw_direct_B = Geodesic.WGS84.Direct(float(rw_lat),float(rw_lon),float(rw_heading+90.0),(float(rw_width))/2)
			B_lat = rw_direct_B.get("lat2")
			B_lon = rw_direct_B.get("lon2")
			
			rw_direct_C = Geodesic.WGS84.Direct(float(rw_lat_end),float(rw_lon_end),-360.0 + float(rw_heading_end)-90.0,(float(rw_width))/2)
			C_lat = rw_direct_C.get("lat2")
			C_lon = rw_direct_C.get("lon2")
			
			rw_direct_D = Geodesic.WGS84.Direct(float(rw_lat_end),float(rw_lon_end),-360.0 + float(rw_heading_end)+90.0,(float(rw_width))/2)
			D_lat = rw_direct_D.get("lat2")
			D_lon = rw_direct_D.get("lon2")
			
			
			insert_runway(ap_identifier,rw_id,rw_id_end,rw_width,rw_lon,rw_lat,rw_lon_end,rw_lat_end,rw_length_meters,rw_length_feet,rw_heading,rw_heading_end,\
			A_lat,A_lon,B_lat,B_lon,C_lat,C_lon,D_lat,D_lon)
			
			# Direct thresholds
			thre_dir_lat = str(rw_threshold_direct.get("lat2"))
			thre_dir_lon = str(rw_threshold_direct.get("lon2"))
			thre_dir_lat_end = str(rw_threshold_direct_end.get("lat2"))
			thre_dir_lon_end = str(rw_threshold_direct.get("lon2"))
			
			#insert_threshold(ap_identifier,rw_id,rw_id_end,thre_dir_lat,thre_dir_lon,thre_dir_lat_end,thre_dir_lon_end)
			
			print "Airport: "+ap_identifier+ " " + "Runway: " + rw_id + ", " + rw_id_end
		
		# Helipads
		if line.startswith("102 "):
		
			helipad = apt.createElement("helipad")
			airport.appendChild(helipad)
			
			hp_linecode = line[0:3]
			generate_node(helipad,"linecode",hp_linecode,1)
			
			hp_designator = line[4:6]
			generate_node(helipad,"designator",hp_designator,1)
			
			hp_lat = line[7:20]
			generate_node(helipad,"latitude",hp_lat,1)
			
			hp_lon = line[21:34]
			generate_node(helipad,"longitude",hp_lon,1)
			
			hp_orientation = line[35:41]
			generate_node(helipad,"orientation",hp_orientation,1)
			
			hp_width = line[42:49]
			generate_node(helipad,"width",hp_width,1)
			
			hp_length = line[50:57]
			generate_node(helipad,"length",hp_length,1)
			
			hp_surface = line[60:61].replace(" ","")
			generate_node_with_attribute(helipad,"surface",str(gethelipadsurface(hp_surface)),"code",hp_surface,0)
			
			hp_markings = line[62:63].replace(" ","")
			generate_node_with_attribute(helipad,"markings",str(gethelipadmarking(hp_markings)),"code",hp_markings,0)
			
			hp_shoulder_surface = line[64:67].replace(" ","")
			generate_node_with_attribute(helipad,"shoulder_surface",str(gethelipadshouldersurface(hp_shoulder_surface)),"code",hp_shoulder_surface,0)
			
			hp_smoothness = line[68:72]
			generate_node(helipad,"smoothness",hp_smoothness,1)
			
			hp_edgelighting = line[73:74]
			generate_node_with_attribute(helipad,"edge_lighting",str(gethelipadedgelighting(hp_edgelighting)),"code",hp_edgelighting,0)
			
		# Viewpoints
		if line.startswith("14 "):
			
			viewpoint = apt.createElement("viewpoint")
			airport.appendChild(viewpoint)
			
			vp_linecode = line[0:3]
			generate_node(viewpoint,"linecode",vp_linecode,1)
			
			vp_latitude = line[4:17]
			generate_node(viewpoint,"latitude",vp_latitude,1)
			
			vp_longitude = line[18:31]
			generate_node(viewpoint,"longitude",vp_longitude,1)
			
			vp_height = line[32:35]
			generate_node(viewpoint,"height",vp_height,1)
			
			vp_deprecated = line[36:37]
			generate_node(viewpoint,"deprecated",vp_deprecated,1)
			
			vp_name_end = len(line)
			vp_name = line[38:vp_name_end-2]
			generate_node(viewpoint,"name",vp_name,0)
			
		# Startup locations
		if line.startswith("15 "):
			
			startuplocation = apt.createElement("startuplocation")
			airport.appendChild(startuplocation)
			
			sl_linecode = line[0:3]
			generate_node(startuplocation,"linecode",sl_linecode,1)
			
			sl_latitude = line[4:17]
			generate_node(startuplocation,"latitude",sl_latitude,1)
			
			sl_longitude = line[18:31]
			generate_node(startuplocation,"longitude",sl_longitude,1)
			
			sl_heading = line[32:37]
			generate_node(startuplocation,"heading",sl_heading,1)
			
			sl_name_end = len(line)
			sl_name = line[38:sl_name_end-2]
			generate_node(startuplocation,"name",sl_name,0)
			
		# Light beacon
		if line.startswith("18 "):
			
			lightbeacon = apt.createElement("lightbeacon")
			airport.appendChild(lightbeacon)
			
			lb_linecode = line[0:3]
			generate_node(lightbeacon,"linecode",lb_linecode,1)
			
			lb_latitude = line[4:16]
			generate_node(lightbeacon,"latitude",lb_latitude,1)
			
			lb_longitude = line[17:31]
			generate_node(lightbeacon,"longitude",lb_longitude,1)
			
			lb_type = line[31:32]
			generate_node_with_attribute(lightbeacon,"type",str(getlightbeacontype(lb_type)),"code",lb_type,0)
			
			lb_description_end = len(line)
			lb_description = line[33:lb_description_end-2]
			generate_node(lightbeacon,"description",lb_description,0)
			
		# Windsock
		if line.startswith("19 "):
			
			windsock = apt.createElement("windsock")
			airport.appendChild(windsock)
			
			ws_linecode = line[0:3]
			generate_node(windsock,"linecode",ws_linecode,1)
			
			ws_latitude = line[4:16]
			generate_node(windsock,"latitude",ws_latitude,1)
			
			ws_longitude = line[17:31]
			generate_node(windsock,"longitude",ws_longitude,1)
			
			ws_lighting = line[31:32]
			generate_node_with_attribute(windsock,"lighting",str(getwindsocklighting(ws_lighting)),"code",ws_lighting,0)
			
			ws_description_end = len(line)
			ws_description = line[33:ws_description_end-2]
			generate_node(windsock,"description",ws_description,0)
			
		# Signs
		if line.startswith("20 "):
			
			sign = apt.createElement("sign")
			airport.appendChild(sign)
			
			si_linecode = line[0:3]
			generate_node(sign,"linecode",si_linecode,1)
			
			si_latitude = line[4:16]
			generate_node(sign,"latitude",si_latitude,1)
			
			si_longitude = line[17:30]
			generate_node(sign,"longitude",si_longitude,1)
			
			si_orientation = line[31:37]
			generate_node(sign,"orientation",si_orientation,1)
			
			si_reserved = line[37:40]
			generate_node(sign,"reserved",si_reserved,1)
			
			si_size = line[41:42].replace(" ","")
			generate_node_with_attribute(sign,"size",str(getsignsize(si_size)),"code",si_size,0)
			
			si_text_end = len(line)
			si_text = line[43:si_text_end-2]
			generate_node(sign,"text",si_text,1)
			
			
		# Lighting Objects
		if line.startswith("21 "):
			
			lightingobject = apt.createElement("lightingobject")
			airport.appendChild(lightingobject)
			lo_rwy_id = line[48:52]
			lightingobject.setAttribute("id", lo_rwy_id.replace(" ",""))
			
			lo_linecode = line[0:3]
			generate_node(lightingobject,"linecode",lo_linecode,1)
			
			lo_latitude = line[4:16]
			generate_node(lightingobject,"latitude",lo_latitude,1)
			
			lo_longitude = line[17:30]
			generate_node(lightingobject,"longitude",lo_longitude,1)
			
			lo_type = line[31:33].replace(" ","")
			generate_node_with_attribute(lightingobject,"type",str(getlightingobjecttype(lo_type)),"code",lo_type,0)
			
			lo_orientation = line[34:39]
			generate_node(lightingobject,"orientation",lo_orientation,1)
			
			lo_glideslope = line[41:47]
			generate_node(lightingobject,"glideslope",lo_glideslope,1)
			
			lo_runway = line[48:51]
			generate_node(lightingobject,"runway",lo_runway,1)
			
			lo_description_end = len(line)
			lo_description = line[52:lo_description_end-2]
			generate_node(lightingobject,"description",lo_description,0)
			
		
		# ATC frequencies
		if line.startswith("50 "):
			atc_recorded = apt.createElement("atc")
			airport.appendChild(atc_recorded)
			atc_recorded.setAttribute("type", "AWOS, ASOS or ATIS")
			atc_linecode = line[0:2]
			generate_node(atc_recorded,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_recorded,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_recorded,"description",atc_description,0)
			
		if line.startswith("51 "):
			atc_unicom = apt.createElement("atc")
			atc_unicom.setAttribute("type", "Unicom (US), CTAF (US), Radio (UK)")
			airport.appendChild(atc_unicom)
			atc_linecode = line[0:2]
			generate_node(atc_unicom,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_unicom,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_unicom,"description",atc_description,0)
			
		if line.startswith("52 "):
			atc_cld = apt.createElement("atc")
			atc_cld.setAttribute("type", "Clearance Delivery")
			airport.appendChild(atc_cld)
			atc_linecode = line[0:2]
			generate_node(atc_cld,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_cld,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_cld,"description",atc_description,0)
			
		if line.startswith("53 "):
			atc_gnd = apt.createElement("atc")
			atc_gnd.setAttribute("type", "Ground")
			airport.appendChild(atc_gnd)
			atc_linecode = line[0:2]
			generate_node(atc_gnd,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_gnd,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_gnd,"description",atc_description,0)
			
		if line.startswith("54 "):
			atc_twr = apt.createElement("atc")
			atc_twr.setAttribute("type", "Tower")
			airport.appendChild(atc_twr)
			atc_linecode = line[0:2]
			generate_node(atc_twr,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_twr,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_twr,"description",atc_description,0)
			
		if line.startswith("55 "):
			atc_app = apt.createElement("atc")
			atc_app.setAttribute("type", "Approach")
			airport.appendChild(atc_app)
			atc_linecode = line[0:2]
			generate_node(atc_app,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_app,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_app,"description",atc_description,0)
			
		if line.startswith("56 "):
			atc_dep = apt.createElement("atc")
			atc_dep.setAttribute("type", "Departure")
			airport.appendChild(atc_dep)
			atc_linecode = line[0:2]
			generate_node(atc_dep,"linecode",atc_linecode,1)
			atc_frequency = line[3:8]
			atc_frequency_float = float(atc_frequency)/100
			generate_node_with_attribute(atc_dep,"frequency",str(atc_frequency_float),"raw",atc_frequency,0)
			atc_description_end = len(line)
			atc_description = line[9:atc_description_end-2]
			generate_node(atc_dep,"description",atc_description,0)

			
readapt()

insert_airport(ap_identifier_ins, ap_name_ins, ap_elevation_ins)

conn.commit()
cur.close()
conn.close()

print "------------------"

