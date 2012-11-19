"""The application's model objects"""


from sqlalchemy import  Integer, String, Date, DateTime
from geoalchemy import  Column, GeometryColumn, GeometryDDL, Point, Polygon, MultiPoint
#from geoalchemy import *
from geoalchemy.postgis import PGComparator
from shapely import wkb;

from fgx.model.meta import Session, Base


def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)
   
FGX_SRID = 3857


##=======================================================
class Airport(Base):
	
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
class Aero(Base):
	
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
class BookMark(Base):
	
	__tablename__ = "bookmark"
	
	bookmark_pk = Column(Integer(), primary_key=True) 
	
	name = Column(String(100), index=True)
	lat = Column(String(15))
	lon = Column(String(15))
	zoom = Column(Integer())

	
	
##=======================================================
class Country(Base):
	
	__tablename__ = "country"
	
	country_code = Column(String(2), primary_key=True)
	country_name = Column(String(100), index=True)

	
##=======================================================
class Dme(Base):
	
	__tablename__ = "dme"
	
	dme_pk = Column(Integer(), primary_key=True)
	ident = Column(String(4), index=True)
	name = Column(String(40), index=True)
	subtype = Column(String(10))
	elevation_m = Column(Integer())	
	freq_mhz = Column(String(10))
	range_km = Column(String(10))
	bias_km = Column(Integer())
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	
GeometryDDL(Dme.__table__)
	

	
class EngineType(Base):
	
	__tablename__ = "engine_type"
		
	engine_pk = Column(Integer(), primary_key=True)
	eng = Column(String(1), unique=True, index=True)
	engine = Column(String(10), unique=True, index=True)
	

	
##=======================================================
# SELECT st_y(wkb_geometry) as lat, st_x(wkb_geometry) as lon, ident FROM fix limit 10;

class Fix(Base):
	
	__tablename__ = 'fix'
	
	fix_pk = Column(Integer(), primary_key=True)
	ident = Column(String(10), index=True, nullable=False)
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)	
	
	@property
	def lat(self):
		return wkb.loads(str(self.wkb_geometry.geom_wkb)).x
		
	@property
	def lon(self):
		return wkb.loads(str(self.wkb_geometry.geom_wkb)).y
	
	def dic(self):
		return dict(ident=self.ident, nav_type="fix",
					lat=self.lat, lon=self.lon)
				
GeometryDDL(Fix.__table__)

##=======================================================
class Ils(Base):
	
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


class Manufacturer(Base):
	
	__tablename__ = "manufacturer"
	
	manuf_pk = Column(Integer(), primary_key=True)
	manuf = Column(String(20), unique=True, index=True)
	
	"""
	manufacturer varchar, \
			model varchar, \
			type_designator varchar, \
			engines varchar, \
			weight_class varchar, \
			climb_rate varchar, \
			descent_rate varchar, \
			srs varchar, \
			LAHSO_group);
	"""
	

##=================================================================
## MpServer
##=================================================================
class MpServer(Base):
	
	__tablename__ = 'mp_server'
	
	MP_STATUS_CHOICES = (
		('unknown', 'Unknown'),
		('up', 'Up'),
		('down', 'Down')
	)
	no = Column(Integer(), primary_key=True)
	subdomain = Column(String(100), index=True) 
	fqdn = Column(String(100), index=True, unique=True) 
	ip = Column(String(16), index=True)
	last_checked = Column(DateTime(), index=True, nullable=True)
	last_seen = Column(DateTime(timezone=False), index=True, nullable=True)
	country = Column(String(100), nullable=True)
	lag = Column(Integer(), nullable=True)
	status = Column(String(20))
	
	lat = Column(String(20), nullable=True)
	lon = Column(String(20), nullable=True)
	#wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
	country = Column(String(50), nullable=True)
	time_zone = Column(String(50), nullable=True)

	def __unicode__(self):
		return self.fqdn
		
		
	def dic(self):
		return { 'no': self.no,
				'fqdn': self.fqdn,
				'ip': self.ip,
				'country': self.country,
				'last_checked': str(self.last_checked),
				'last_seen': str(self.last_seen) if self.last_seen else None,
				'lag': self.lag,
				'lat': self.lat,
				'lon': self.lon,
				'country': self.country,
				'time_zone': self.time_zone
		}
		
		
		
	@staticmethod
	def fqdn_from_no(server_no):
		return "mpserver%02d.flightgear.org" % server_no
	
	@staticmethod
	def subdomain_from_no(server_no):
		return "mpserver%02d" % server_no	
		
		
##=================================================================
## Bot Info
##=================================================================

## Records when the bot last did a DNS check
class MpBotInfo(Base):
	
	__tablename__ = "mp_bot_info"

	id = Column(Integer(), primary_key=True)
	
	last_dns_start = Column(DateTime())
	last_dns_end = Column(DateTime())
	
	last_check_start = Column(DateTime())
	last_check_end = Column(DateTime())

##=======================================================
class NavAids(Base):
	
	__tablename__ = "navaid"
	
	navaid_pk = Column(Integer(), primary_key=True)
	
	nav_type = Column(String(10), index=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq = Column(String(10), index=True)
	
	elevation_ft = Column(Integer(), nullable=True)
	elevation_m = Column(Integer(), nullable=True)
	range_nm = Column(Integer(), nullable=True)
	range_m = Column(Integer(), nullable=True)
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
	
	## MAYBE these props need to strings
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
				'elevation_ft': self.elevation_ft,
				'elevation_m': self.elevation_m,
				'range_nm': self.range_nm,
				'range_m': self.range_m,
		}
		
GeometryDDL(NavSearch.__table__)	
		

##=======================================================
class Ndb(Base):
	
	__tablename__ = "ndb"
	
	ndb_pk = Column(Integer(), primary_key=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq_khz = Column(String(6))
	
	elevation_ft = Column(Integer(), nullable=True)
	elevation_m = Column(Integer(), nullable=True)
	range_nm = Column(Integer(), nullable=True)
	range_m = Column(Integer(), nullable=True)
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	## These can go later
	lat = Column(String(15), index=True, nullable=False)
	lon = Column(String(15), index=True, nullable=False)
	
	def __repr__(self):
		return "<Ndb: %s>" % (self.ident)
		
	def dic(self):
		return dict(ident=self.ident, name=self.name, nav_type="ndb",
				lat=self.lat, lon=self.lon)
		
GeometryDDL(Ndb.__table__)		


##=======================================================
class Runway(Base):
	
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
class Threshold(Base):
	
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
	

##=======================================================
class Vor(Base):
	
	__tablename__ = "vor"
	
	vor_pk = Column(Integer, primary_key=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq_mhz = Column(String(6))
	
	elevation_ft = Column(Integer(), nullable=True)
	elevation_m = Column(Integer(), nullable=True)
	range_nm = Column(Integer(), nullable=True)
	range_m = Column(Integer(), nullable=True)
	
	# TODO What is this exactly ?
	variation = Column(String(10), nullable=True)
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	## These can go later
	lat = Column(String(15), index=True, nullable=False)
	lon = Column(String(15), index=True, nullable=False)
	
	def __repr__(self):
		return "<Vor: %s>" % (self.ident)

	def dic(self):
		return dict(ident=self.ident, name=self.name, nav_type="vor",
				lat=self.lat, lon=self.lon, )
		
GeometryDDL(Vor.__table__)


##=======================================================
class User(Base):
	
	__tablename__ = "user"
	
	user_pk = Column(Integer, primary_key=True)
	
	email = Column(String(50), index=True, nullable=False)
	name = Column(String(50), index=True, nullable=False)
	callsign = Column(String(10), nullable=False)
	passwd = Column(String(100), nullable=False)
	
	## Security level.. idea atmo is 0 = disabled, 1 = Auth, 2 = Admin, 
	level = Column(Integer, nullable=False)
	
	created = Column(DateTime(), nullable=False)
	
	


