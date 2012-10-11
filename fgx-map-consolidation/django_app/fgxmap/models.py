

from django.db import models
from django.contrib.gis.db import models

"""
Pete's guidelines

* make the table names singular, avoids problems with 's's
* needs a *_pk field each table, - use pk not is as avoid poss name clash

"""



SRID = 3857 # ?? gral ?

##=======================================================
class Airport(models.Model):
	
	class Meta:
		db_table = "airport"
	
	apt_pk = models.IntegerField(primary_key=True) 
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
	
	class Meta:
		db_table = "dme"
	
	dme_pk = models.IntegerField(primary_key=True)
	ident = models.CharField(max_length=4, db_index=True)
	name = models.CharField(max_length=40, db_index=True)
	subtype = models.CharField(max_length=10)
	elevation_m = models.IntegerField()
	freq_mhz = models.CharField(max_length=10)
	range_km = models.CharField(max_length=10)
	bias_km = models.IntegerField()
	geom = models.PointField(srid=SRID)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	


##=======================================================
class Fix(models.Model):
	
	class Meta:
		db_table = "fix"
		verbose_name = "fix"
		verbose_name_plural = "fix"
	
	fix_pk = models.IntegerField( primary_key=True)
	fix = models.CharField(max_length=10, db_index=True)	
	geom = models.PointField(srid=SRID)

	def __repr__(self):
		return "<Fix: %s>" % (self.fix)
	




##=======================================================
class Runway(models.Model):
	
	class Meta:
		db_table = "runway"
	
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
	
	geom = models.MultiPolygonField(srid=SRID)
	
	def __repr__(self):
		return "<Threshold: %s-%s>" % (self.apt_icao, self.rwy)
	

