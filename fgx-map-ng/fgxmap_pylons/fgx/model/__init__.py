"""The application's model objects"""


from sqlalchemy import Column, Integer, String, Date, DateTime
from geoalchemy import  GeometryColumn, GeometryDDL, Point, Polygon
from geoalchemy.postgis import PGComparator


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
	apt_elev_ft = Column(Integer(10), nullable=True)
	apt_elev_m = Column(Integer(10), nullable=True)
	apt_authority = Column(Integer(10), nullable=True)
	apt_services = Column(Integer(10), nullable=True)
	apt_ifr = Column(Integer(10), nullable=True)
	apt_size = Column(Integer(10), nullable=True)
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
class Fix(Base):
	
	__tablename__ = 'fix'
	
	fix_pk = Column(Integer(), primary_key=True)
	fix = Column(String(10), index=True, nullable=False)
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
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
	apt_elev_ft = Column(Integer(10), nullable=True)
	apt_elev_m = Column(Integer(10), nullable=True)
	apt_authority = Column(Integer(10), nullable=True)
	apt_services = Column(Integer(10), nullable=True)
	apt_ifr = Column(Integer(10), nullable=True)
	apt_size = Column(Integer(10), nullable=True)
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

	def __unicode__(self):
		return self.fqdn
		
		
	def dic(self):
		return { 'no': self.no,
				'fqdn': self.fqdn,
				'ip': self.ip,
				'country': self.country,
				'last_checked': str(self.last_checked),
				'last_seen': str(self.last_checked) if self.last_checked else None,
				'lag': self.lag
				
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
class Ndb(Base):
	
	__tablename__ = "ndb"
	
	ndb_pk = Column(Integer(), primary_key=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq_khz = Column(String(6))
	
	elevation_ft = Column(Integer())
	elevation_m = Column(Integer())
	range_nm = Column(Integer())
	range_m = Column(Integer())
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Ndb: %s>" % (self.ident)
		
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
	
	elevation_ft = Column(Integer())
	elevation_m = Column(Integer())
	range_nm = Column(Integer())
	range_m = Column(Integer())
	
	# TODO What is this exactly ?
	variation = Column(String(10))
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Vor: %s>" % (self.ident)
		
GeometryDDL(Vor.__table__)


#class WeightClass(Base):




