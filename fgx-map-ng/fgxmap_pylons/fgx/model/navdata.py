##@package fgx.model.navdata 
# @brief Navigation, airport data and postgis database models
#
# @warning Required postgis

from sqlalchemy import  Integer, String, Date, DateTime
from geoalchemy import  Column, GeometryColumn, GeometryDDL, Point, Polygon, MultiPoint, LineString
from geoalchemy.postgis import PGComparator
from shapely import wkb

from sqlalchemy import  Integer, String, Date, DateTime, Column
from sqlalchemy.dialects.postgresql import ARRAY
from fgx.model.meta import Sess, Base


FGX_SRID = 3857

##################################################
"""
class Airway(Base.navdata):
	
	__tablename__ = "airway"
	
	awy_pk = Column(Integer(), primary_key=True)
	ident_entry = Column(String(4), index=True)
	ident_exit = Column(String(4), index=True)
	apt_iata = Column(String(8), index=True, nullable=True)
	apt_name = Column(String(40), index=True, nullable=True)
	apt_country = Column(String(2), nullable=True)
	apt_type = Column(String(4), nullable=True)
"""	
##################################################
"""
class AirwaySegment(Base.navdata):
	
	LOW = 1
	HIGHT = 2
	
	__tablename__ = "airway_segment"
	
	awy_seg_pk = Column(Integer(), primary_key=True)
	name = Column(String(30), index=True)
	
	ident_entry = Column(String(10), index=True)
	ident_exit = Column(String(10), index=True)
	
	wkb_geometry = GeometryColumn(LineString(srid=FGX_SRID), comparator=PGComparator, nullable=True)
	
	level = Column(Integer()) #, index=True)
	fl_base = Column(Integer()) #, index=True)
	fl_top = Column(Integer()) #, index=True)
	

	
	airway = Column(String(255)) #, index=True)
	search = Column(String(255)) #, index=True)
	
GeometryDDL(AirwaySegment.__table__)	
"""	
	
	
##################################################
class Airport(Base.navdata):
	
	__tablename__ = "airport"
	
	apt_pk = Column(Integer(), primary_key=True)
	apt_ident = Column(String(8), index=True)
	apt_local_code = Column(String(8), index=True, nullable=True)
	
	apt_name_ascii = Column(String(255), index=True, nullable=True)
	apt_name_utf8 = Column(String(255), index=True, nullable=True)
	
	apt_country = Column(String(8), nullable=True)
	apt_type = Column(String(50), nullable=True)
	
	apt_elev_ft = Column(String(32), nullable=True)
	apt_elev_m = Column(String(32), nullable=True)
	apt_authority = Column(String(32), nullable=True)
	apt_services = Column(String(1), nullable=True)
	apt_ifr = Column(String(1), nullable=True)
	apt_size = Column(String(32), nullable=True)
	
	#if POSTGIS: #INTERESTING said pete
	apt_center = GeometryColumn(Point(srid=FGX_SRID), comparator=PGComparator, nullable=True)
	apt_center_lat = Column(String(32), nullable=True)
	apt_center_lon = Column(String(32), nullable=True)
	apt_center_lat84 = Column(String(32), nullable=True)
	apt_center_lon84 = Column(String(32), nullable=True)
	
	apt_rwy_count = Column(String(20), nullable=True)
	apt_min_rwy_len_ft = Column(String(20), nullable=True)
	apt_max_rwy_len_ft = Column(String(20), nullable=True)
	apt_xplane_code = Column(String(20), nullable=True)

	def dic(self):
		return dict(
			apt_pk=self.apt_pk, apt_ident=self.apt_ident, apt_local_code=self.apt_local_code,
			apt_name_ascii=self.apt_name_ascii, apt_type=self.apt_type,
			apt_elev_ft=self.apt_elev_ft,
			apt_elev_m=self.apt_elev_m,
			apt_authority=self.apt_authority,
			apt_services=self.apt_services,
			apt_ifr=self.apt_ifr,
			apt_size=self.apt_size,
			apt_center_lat=self.apt_center_lat,
			apt_center_lon=self.apt_center_lon,
			apt_center_lat84=self.apt_center_lat84,
			apt_center_lon84=self.apt_center_lon84,
			apt_min_rwy_len_ft=self.apt_min_rwy_len_ft,
			apt_max_rwy_len_ft=self.apt_max_rwy_len_ft,
			apt_xplane_code=self.apt_xplane_code
		)
	
	def __repr__(self):
		return "<Airport: %s>" % (self.apt_ident)


GeometryDDL(Airport.__table__)


	
##################################################
class Aero(Base.navdata):
	
	__tablename__ = "aircraft"
	
	aero_pk = Column(Integer(), primary_key=True) 
	#manufacturers = models.Remotekey()
	
	model = Column(String(10), unique=True, index=True)
	type_designator = Column(String(10))
	
	engines = Column(Integer())
	engine_type = Column(String(1))
	
	weight_class = Column(String(40))
	
	climb_rate_fpm = Column(String(40))
	descent_rate_fpm = Column(String(40))
	
	srs = Column(String(40))
	lahso = Column(Integer())
	
	
	
##################################################
class Country(Base.navdata):
	
	__tablename__ = "country"
	
	country_code = Column(String(2), primary_key=True)
	country_name = Column(String(100), index=True)

	
##################################################	
class Fix(Base.navdata):
	
	__tablename__ = 'fix'
	
	fix_pk = Column(Integer(), primary_key=True)
	fix_ident = Column(String(10), index=True, nullable=False)
	fix_center = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	fix_center_lat = Column(String(32), nullable=False)
	fix_center_lon = Column(String(32), nullable=False)
	fix_center_lat84 = Column(String(32), nullable=False)
	fix_center_lon84 = Column(String(32), nullable=False)
	
	
	def dic(self):
		
		return dict(
			fix_ident=self.fix_ident, 
			fix_center_lat=self.fix_center_lat, fix_center_lon=self.fix_center_lon,
			fix_center_lat84=self.fix_center_lat84, fix_center_lon84=self.fix_center_lon84
		)
		

GeometryDDL(Fix.__table__)	
	
##################################################
class Ils(Base.navdata):
	
	__tablename__ = "ils"
	
	ils_pk = Column(Integer(), primary_key=True)
	threshold_pk = Column(Integer())
	apt_ident = Column(String(4), index=True)
	apt_iata = Column(String(8), index=True, nullable=True)
	apt_name = Column(String(40), index=True, nullable=True)
	apt_country = Column(String(2), nullable=True)
	apt_type = Column(String(4), nullable=True)
	apt_elev_ft = Column(Integer(), nullable=True)
	apt_elev_m = Column(Integer(), nullable=True)
	apt_authority = Column(Integer(), nullable=True)
	apt_services = Column(Integer(), nullable=True)
	apt_ifr = Column(Integer(), nullable=True)
	apt_size = Column(Integer(), nullable=True)
	apt_center = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator, nullable=True)
	apt_center_lat = Column(String(20), nullable=True)
	apt_center_lon = Column(String(20), nullable=True)
	apt_rwy_count = Column(Integer(), nullable=True)
	apt_min_rwy_len_ft = Column(Integer(), nullable=True)
	apt_max_rwy_len_ft = Column(Integer(), nullable=True)
	apt_xplane_code = Column(Integer(), nullable=True)
	#wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Airport: %s>" % (self.apt_ident)


GeometryDDL(Airport.__table__)



##################################################
class NavAid(Base.navdata):
	
	class TYPE:
		
		fix = "FIX"
		
		lda_gs = "LDA-GS"
		tacan = "TACAN"
		vortac = "VORTAC"
		lom = "LOM"
		
		ndb = "NDB"
		ndb_dme = "NDB-DME"
		
		dme = "DME"
		
		vor = "VOR"
		vor_dme = "VOR-DME"
		
		
		
	
	__tablename__ = "navaid"
	
	nav_pk = Column(Integer(), primary_key=True)
	
	
	nav_type = Column(String(10), index=True)
	
	nav_ident = Column(String(32), index=True)
	apt_ident = Column(String(8), index=True)
	rwy_ident = Column(String(8), index=True)
	
	nav_name = Column(String(255), index=True)
	nav_suffix =  Column(String(32), index=True)
	
	nav_bearing_true = Column(String(32))
	nav_var_deg = Column(String(32))
	
	nav_freq_khz = Column(String(32))
	nav_freq_mhz = Column(String(32))
	
	nav_elev_ft = Column(String(10))
	#nav_elev_m = Column(String(10))
	
	
	#range_m = Column(String(10))
	
	nav_center = GeometryColumn(Point(2, srid=3857), comparator=PGComparator)
	nav_center_lon = Column(String(32))
	nav_center_lat = Column(String(32))
	nav_center_lon84 = Column(String(32))
	nav_center_lat84 = Column(String(32))
	
	nav_range_nm = Column(String(10))
	nav_range_poly = GeometryColumn(Polygon(srid=3857), comparator=PGComparator)
	
	nav_bias_nm = Column(String(32))
	nav_standalone = Column(String(8))
	nav_no_freq = Column(String(8))
	nav_xplane_code = Column(String(8))
	
	
	## MAYBE these props need to return strings ?
	@property
	def lat(self):
		return wkb.loads(str(self.wkb_geometry.geom_wkb)).x	
	@property
	def lon(self):
		return wkb.loads(str(self.wkb_geometry.geom_wkb)).y

	def __repr__(self):
		return "<NavAid: %s>" % (self.ident)
		
	def dic(self):
		return { 'nav_type': self.nav_type,
				'ident': self.ident,
				'name': self.name,
				'lat': self.lat,
				'lon': self.lon,
				'elev_ft': self.elev_ft,
				'elev_m': self.elev_m,
				'range_nm': self.range_nm,
				'range_m': self.range_m,
		}
		
GeometryDDL(NavAid.__table__)	
		

	


##################################################
class Runway(Base.navdata):
	
	__tablename__ = "runway"
	
	rwy_pk = Column(Integer(), primary_key=True)
	apt_ident = Column(String(8), index=True)
	rwy_ident = Column(String(8), index=True)
	rwy_ident_end = Column(String(8))
	
	rwy_width = Column(String(32))
	
	rwy_lat84 = Column(String(32))
	rwy_lon84 = Column(String(32))
	
	rwy_lat84_end = Column(String(32))
	rwy_lon84_end = Column(String(32))

	rwy_len_m = Column(String(32))
	rwy_len_ft = Column(String(32))
	
	rwy_hdg = Column(String(32))
	rwy_hdg_end = Column(String(32))
	
	rwy_shoulder = Column(String(8))
	rwy_smoothness = Column(String(8))
	rwy_surface = Column(String(32))
	
	rwy_centerline_lights = Column(String(8))
	rwy_edge_lighting = Column(String(8))
	rwy_auto_dist_signs = Column(String(8))
	
	
	rwy_threshold = Column(String(32))
	rwy_overrun = Column(String(32))
	rwy_marking = Column(String(8))
	rwy_app_lighting = Column(String(8))
	rwy_tdz_lighting = Column(String(8))
	rwy_reil = Column(String(8))
	
	rwy_threshold_end = Column(String(32))
	rwy_overrun_end = Column(String(32))
	rwy_marking_end = Column(String(8))
	rwy_app_lighting_end = Column(String(8))
	rwy_tdz_lighting_end = Column(String(8))
	rwy_reil_end = Column(String(8))	
	
	rwy_xplane_code = Column(String(8))	
	
	rwy_poly = GeometryColumn(Polygon(srid=FGX_SRID), comparator=PGComparator)

	@property
	def rwy(self):
		return "%s-%s" % (self.rwy_ident.strip(), self.rwy_ident_end.strip())
	
	def __repr__(self):
		return "<Runway: [%s] %s-%s>" % (self.apt_ident, self.rwy_ident, self.rwy_ident_end)
		
	def tree(self):
		
		return  dict(
			apt_ident=self.apt_ident,
			rwy=self.rwy,
			rwy_len_m = self.rwy_len_m,
			thresholds= [ self.threshold(0), self.threshold(1) ]		
		)
	
	##@property
	def threshold(self, end=False):
		props = ["rwy_threshold", "rwy_ident", "rwy_reil", "rwy_marking", "rwy_overrun", "rwy_app_lighting"]
		postfix = "_end" if end else ""
		dic = {}
		for p in props:
			dic[p] = getattr(self, p + postfix)
		return dic
		
	def dic(self):
		return dict(
			apt_ident = self.apt_ident,
			rwy_ident = self.rwy_ident,
			rwy_width = self.rwy_width,
			rwy_lat = self.rwy_lat,	rwy_lon = self.rwy_lon,
			rwy_lat_end = self.rwy_lat_end,	rwy_lon_end = self.rwy_lon_end,
			rwy_len_meters = self.rwy_len_meters,
			rwy_len_feet = self.rwy_len_feet,
			
			rwy_hdg = self.rwy_hdg,
			rwy_hdg_end = self.rwy_hdg_end,
			rwy_threshold = self.rwy_threshold,
			rwy_threshold_end = self.rwy_threshold_end
		)
	
GeometryDDL(Runway.__table__)	

##################################################
"""
class Threshold(Base.navdata):
	
	__tablename__ = "threshold"

	threshold_pk = Column(Integer(), primary_key=True)
	rwy_id = Column(String(5), index=True)
	apt_icao = Column(String(10), index=True)
	rwy = Column(String(10), index=True)
	
	overrun_id = Column(Integer(), index=True)
	marking_id = Column(Integer(), index=True)
	appr_light_id = Column(Integer(), index=True)
	tdz_light_id = Column(Integer(), index=True)
	
	geom = GeometryColumn(Polygon(srid=FGX_SRID), comparator=PGComparator)
	
	def __repr__(self):
		return "<Threshold: %s-%s>" % (self.apt_icao, self.rwy)
	

GeometryDDL(Threshold.__table__)	
"""



	