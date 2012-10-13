


from django.contrib.gis.db import models

from settings import FGX_SRID



##=======================================================
class Dme(models.Model):
	
	class Meta:
		db_table = "dme"
	
	dme_pk = models.AutoField(primary_key=True)
	ident = models.CharField(max_length=4, db_index=True)
	name = models.CharField(max_length=40, db_index=True)
	subtype = models.CharField(max_length=10)
	elevation_m = models.IntegerField()
	freq_mhz = models.CharField(max_length=10)
	range_km = models.CharField(max_length=10)
	bias_km = models.IntegerField()
	wkb_geometry = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	


	
	
	
##=======================================================
class Fix(models.Model):
	
	class Meta:
		db_table = "fix"
		verbose_name = "fix"
		verbose_name_plural = "fix"
	
	fix_pk = models.AutoField( primary_key=True)
	fix = models.CharField(max_length=10, db_index=True, unique=True)	
	wkb_geometry = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Fix: %s>" % (self.fix)
	
	@property
	def lat(self):
		return str(self.wkb_geometry.coords[0])
	
	@property
	def lon(self):
		return str(self.wkb_geometry.coords[1])
		
	## Returns data in python dic - this is a bit of a jhack and subject to change
	# @retval data as dict
	def dic(self):
		
		return dict(
				fix = self.fix,
				fix_pk = self.fix_pk,
				lat = self.lat, 
				lon = self.lon
		)
	
	
	
##=======================================================
class Ndb(models.Model):
	
	class Meta:
		db_table = "ndb"
	
	ndb_pk = models.AutoField(primary_key=True)
	ident = models.CharField(max_length=4, db_index=True)
	#name = models.CharField(max_length=40, db_index=True)
	#subtype = models.CharField(max_length=10)
	#elevation_m = models.IntegerField()
	freq_mhz = models.CharField(max_length=10)
	range_km = models.CharField(max_length=10)
	bias_km = models.IntegerField()
	wkb_geometry = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	


	
	
