
from sqlalchemy import  Integer, String, Date, DateTime
from geoalchemy import  Column, GeometryColumn, GeometryDDL, Point, Polygon, MultiPoint, LineString
from geoalchemy.postgis import PGComparator
from shapely import wkb

from sqlalchemy import  Integer, String, Date, DateTime, Column
from sqlalchemy.dialects.postgresql import ARRAY
from fgx.model.meta import Sess, Base


FGX_SRID = 3857

##=======================================================
"""
class Airway(Base.data):
	
	__tablename__ = "airway"
	
	awy_pk = Column(Integer(), primary_key=True)
	ident_entry = Column(String(4), index=True)
	ident_exit = Column(String(4), index=True)
	apt_iata = Column(String(8), index=True, nullable=True)
	apt_name = Column(String(40), index=True, nullable=True)
	apt_country = Column(String(2), nullable=True)
	apt_type = Column(String(4), nullable=True)
"""	
##=======================================================
class AirwaySegment(Base.data):
	
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
	
GeometryDDL(AirwaySegment.__table__)	
	
	
	
##=======================================================
class Airport(Base.data):
	
	__tablename__ = "airport"
	
	apt_pk = Column(Integer(), primary_key=True)
	apt_ident = Column(String(4), index=True)
	apt_iata = Column(String(8), index=True, nullable=True)
	apt_name = Column(String(40), index=True, nullable=True)
	apt_country = Column(String(2), nullable=True)
	apt_type = Column(String(4), nullable=True)
	
	apt_elev_ft = Column(Integer(), nullable=True)
	apt_elev_m = Column(Integer(), nullable=True)
	apt_authority = Column(String(4), nullable=True)
	apt_services = Column(String(10), nullable=True)
	apt_ifr = Column(String(10), nullable=True)
	apt_size = Column(String(10), nullable=True)
	
	apt_center = GeometryColumn(MultiPoint(srid=FGX_SRID), comparator=PGComparator, nullable=True)
	apt_center_lat = Column(String(20), nullable=True)
	apt_center_lon = Column(String(20), nullable=True)
	
	apt_rwy_count = Column(Integer(), nullable=True)
	apt_min_rwy_len_ft = Column(Integer(), nullable=True)
	apt_max_rwy_len_ft = Column(Integer(), nullable=True)
	apt_xplane_code = Column(Integer(), nullable=True)
	#wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def dic(self):
		return dict(apt_pk=self.apt_pk, apt_ident=self.apt_ident)
	
	def __repr__(self):
		return "<Airport: %s>" % (self.apt_ident)
	
GeometryDDL(Airport.__table__)


	
##=======================================================
class Aero(Base.data):
	
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
	
	
	
##=======================================================
class Country(Base.data):
	
	__tablename__ = "country"
	
	country_code = Column(String(2), primary_key=True)
	country_name = Column(String(100), index=True)

	

##=======================================================
class Ils(Base.data):
	
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



##=======================================================
class NavAid(Base.data):
	
	class NAV_TYPE:
		
		fix = "FIX"
		ndb = "NDB"
		
		dme = "DME"
		vor = "VOR"
		vor_dme = "VOR-DME"
		vortac = "VORTAC"
		
	
	__tablename__ = "navaid"
	
	navaid_pk = Column(Integer(), primary_key=True)
	
	nav_type = Column(String(10), index=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq = Column(String(10), index=True, nullable=True)
	
	elev_ft = Column(String(10), nullable=True)
	elev_m = Column(String(10), nullable=True)
	range_nm = Column(String(10), nullable=True)
	range_m = Column(String(10), nullable=True)
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
	
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
		

	


##=======================================================
class Runway(Base.data):
	
	__tablename__ = "runway"
	
	rwy_pk = Column(Integer(), primary_key=True)
	apt_ident = Column(String(10), index=True)
	rwy = Column(String(10), index=True)
	length_ft = Column(Integer())
	length_m = Column(Integer())
	geom = GeometryColumn(Polygon(srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Runway: %s-%s>" % (self.icao, self.rwy_id)
	
GeometryDDL(Runway.__table__)	

##=======================================================
class Threshold(Base.data):
	
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
	



	