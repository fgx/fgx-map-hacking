

from django.db import models
from django.contrib.gis.db import models


SRID = 3857 # ?? gral ?

##=======================================================
class Airport(models.Model):
	__tablename__ = "airport"
	
	#apt_pk = Column(Integer, primary_key=True) 
	# Maybe apt_icao is primary key
	apt_icao = models.CharField(max_length=6, unique=True, db_index=True)
	apt_name = models.CharField(max_length=100, db_index=True)
	elevation = models.CharField(max_length=30)
	mpoly = models.PointField(srid=SRID)

	## center lat
	## center lon
	
	def __repr__(self):
		return "<Airport: %s>" % (self.apt_icao)
	




##=======================================================
class Dme(models.Model):
	__tablename__ = "dme"
	
	dme_pk = models.IntegerField(primary_key=True)
	ident = models.CharField(max_length=4), nullable=False, index=True)
	name = models.CharField(max_length=40), nullable=False, index=True)
	subtype = models.CharField(max_length=10), nullable=True)
	elevation_m = Column(Integer(), nullable=True)
	freq_mhz = models.CharField(max_length=10), nullable=True)
	range_km = models.CharField(max_length=10), nullable=True)
	bias_km = Column(Numeric(precision=2, scale=None, as_decimal=True), nullable=True)
	geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	
GeometryDDL(Dme.__table__)

"""

##=======================================================
class Fix(models.Model):
	__tablename__ = "fix"
	
	fix_id = Column(Integer, primary_key=True)
	fix_name = models.CharField(max_length=10), nullable=False, index=True)
	geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Fix: %s>" % (self.icao)
	
GeometryDDL(Fix.__table__)



##=======================================================
class Runway(models.Model):
	__tablename__ = "runway"
	
	rwy_id = Column(Integer, primary_key=True)
	apt_icao = models.CharField(max_length=10), nullable=False, index=True)
	rwy = models.CharField(max_length=10), nullable=False, index=True)
	length = models.CharField(max_length=30), nullable=False)
	geometry = GeometryColumn(Polygon(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Runway: %s-%s>" % (self.icao, self.rwy_id)
	
GeometryDDL(Runway.__table__)





##=======================================================
class Threshold(models.Model):
	__tablename__ = "threshold"

	thresh_id = Column(Integer(), primary_key=True)
	rwy_id = Column(Integer(), index=True)
	apt_icao = models.CharField(max_length=10), nullable=False, index=True)
	rwy = models.CharField(max_length=10), nullable=False, index=True)
	
	overrun_id = Column(Integer(), index=True, nullable=True)
	marking_id = Column(Integer(), index=True, nullable=True)
	appr_light_id = Column(Integer(), index=True, nullable=True)
	tdz_light_id = Column(Integer(), index=True, nullable=True)
	
	geometry = GeometryColumn(Polygon(), srid=3857, spatial_index=True)
	
	def __repr__(self):
		return "<Threshold: %s-%s>" % (self.apt_icao, self.rwy)
	
GeometryDDL(Threshold.__table__)

"""