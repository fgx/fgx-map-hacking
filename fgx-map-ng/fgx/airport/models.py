

from django.contrib.gis.db import models

from settings import FGX_SRID

##=======================================================
class Airport(models.Model):
	
	class Meta:
		db_table = "airport"
	
	apt_pk = models.IntegerField(primary_key=True) 
	apt_icao = models.CharField(max_length=6, unique=True, db_index=True)
	apt_name = models.CharField(max_length=100, db_index=True)
	elevation = models.CharField(max_length=30)
	geom = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	## center lat
	## center lon
	
	def __repr__(self):
		return "<Airport: %s>" % (self.apt_icao)
	




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
	

