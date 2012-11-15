"""The application's model objects"""


from sqlalchemy import Integer, String, Date, DateTime
from geoalchemy import Column, GeometryColumn, GeometryDDL, Point
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
class Aero(models.Model):
	
	class Meta:
		db_table = "aircraft"
	
	aero_pk = models.IntegerField(primary_key=True) 
	#manufacturers = models.Remotekey()
	
	model = models.CharField(max_length=10, unique=True, db_index=True)
	type_designator =  models.CharField(max_length=10)
	
	engines = models.IntegerField()
	engine_type = models.CharField(max_length=1)
	
	weight_class = models.CharField(max_length=40)
	
	climb_rate_fpm = models.CharField(max_length=40)
	descent_rate_fpm = models.CharField(max_length=40)
	
	srs = models.CharField(max_length=40)
	lahso = models.IntegerField()
			


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
	

class EngineType(models.Model):
	engine_pk  models.IntegerField(primary_key=True) 
	eng = models.CharField(max_length=1, unique=True, db_index=True)
	engine = models.CharField(max_length=10, unique=True, db_index=True)
	

	
	
	
##=======================================================	
class Fix(Base):
	
	__tablename__ = 'fix'
	
	fix_pk = Column(Integer(), primary_key=True)
	fix = Column(String(10), index=True, nullable=False)
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
GeometryDDL(Fix.__table__)


class Manufacturer(models.Model):
	class Meta:
		db_table = "manufacturer"
	
	manuf_pk = models.IntegerField(primary_key=True) 
	manuf = models.CharField(max_length=20, unique=True, db_index=True)
	
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
	fqdn = models.CharField(max_length=100, db_index=True, unique=True) 
	ip = models.IPAddressField( db_index=True)
	last_checked = models.DateTimeField(db_index=True, null=True)
	last_seen = models.DateTimeField(db_index=True, null=True)
	country = models.CharField(max_length=100, null=True)
	lag = models.IntegerField(null=True)
	status = models.CharField(max_length=20, choices=MP_STATUS_CHOICES, default="unknown")

	def __unicode__(self):
		return self.fqdn
		
		
	def dic(self):
		return { 'no': self.no,
				'fqdn': self.fqdn,
				'ip': self.ip,
				'country': self.country,
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
	
	last_dns_start = Column(DateTimeField())
	last_dns_end = Column(DateTimeField())
	
	last_check_start = Column(DateTimeField())
	last_check_end = Column(DateTimeField())

		
		

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
class Runway(models.Model):
	
	class Meta:
		db_table = "runway"
	
	rwy_pk = models.AutoField( primary_key=True)
	apt_icao = models.CharField(max_length=10, db_index=True)
	rwy = models.CharField(max_length=10, db_index=True)
	length_ft = models.IntegerField()
	length_m = models.IntegerField()
	geom = models.MultiPolygonField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Runway: %s-%s>" % (self.icao, self.rwy_id)
	


##=======================================================
class Threshold(models.Model):
	
	class Meta:
		db_table = "threshold"

	thresh_pk = models.IntegerField(primary_key=True)
	rwy_id = models.CharField(max_length=5, db_index=True)
	apt_icao = models.CharField(max_length=10, db_index=True)
	rwy = models.CharField(max_length=10, db_index=True)
	
	overrun_id = models.IntegerField(db_index=True)
	marking_id = models.IntegerField(db_index=True)
	appr_light_id = models.IntegerField(db_index=True)
	tdz_light_id = models.IntegerField(db_index=True)
	
	geom = models.MultiPolygonField(srid=FGX_SRID)
	objects = models.GeoManager()
	
	def __repr__(self):
		return "<Threshold: %s-%s>" % (self.apt_icao, self.rwy)
	

	
	

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


#class WeightClass(models.Model):




