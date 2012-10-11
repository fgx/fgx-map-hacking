

from django.db import models
from django.contrib.gis.db import models


SRID = 3857 # ?? gral ?

##=======================================================
class Airport(models.Model):
	__tablename__ = "airport"
	
	#apt_pk = models.Integer, primary_key=True) 
	# Maybe apt_icao is primary key
	apt_icao = models.CharField(max_length=6, unique=True, db_index=True)
	apt_name = models.CharField(max_length=100, db_index=True)
	elevation = models.CharField(max_length=30)
	geom = models.PointField(srid=SRID)

	## center lat
	## center lon
	
	def __repr__(self):
		return "<Airport: %s>" % (self.apt_icao)
	



##=======================================================
class Dme(models.Model):
	__tablename__ = "dme"
	
	dme_pk = models.IntegerField(primary_key=True)
	ident = models.CharField(max_length=4, db_index=True)
	name = models.CharField(max_length=40, db_index=True)
	subtype = models.CharField(max_length=10)
	elevation_m = models.IntegerField()
	freq_mhz = models.CharField(max_length=10)
	range_km = models.CharField(max_length=10)
	bias_km = Column(Numeric(precision=2, scale=None, as_decimal=True), nullable=True)
	geom = models.PointField(srid=SRID)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	


##=======================================================
class Fix(models.Model):
	__tablename__ = "fix"
	
	fix_pk = models.IntegerField( primary_key=True)
	fix_name = models.CharField(max_length=10, db_index=True)
	geom = models.PointField(srid=SRID)

	def __repr__(self):
		return "<Fix: %s>" % (self.icao)
	




##=======================================================
class Runway(models.Model):
	__tablename__ = "runway"
	
	rwy_pk = models.IntegerField( primary_key=True)
	apt_icao = models.CharField(max_length=10, db_index=True)
	rwy = models.CharField(max_length=10, db_index=True)
	length_ft = models.IntegerField()
	length_m = models.IntegerField()
	geom = models.MultiPolygonField(srid=SRID)

	def __repr__(self):
		return "<Runway: %s-%s>" % (self.icao, self.rwy_id)
	





##=======================================================
class Threshold(models.Model):
	__tablename__ = "threshold"

	thresh_pk = models.IntegerField(primary_key=True)
	rwy_id = models.CharField(msx_length=5, db_index=True)
	apt_icao = models.CharField(max_length=10, db_index=True)
	rwy = models.CharField(max_length=10, db_index=True)
	
	overrun_id = models.IntegerField(db_index=True)
	marking_id = models.IntegerField(db_index=True)
	appr_light_id = models.IntegerField(db_index=True)
	tdz_light_id = models.IntegerField(db_index=True)
	
	geom = models.MultiPolygonField(srid=SRID)
	
	def __repr__(self):
		return "<Threshold: %s-%s>" % (self.apt_icao, self.rwy)
	

