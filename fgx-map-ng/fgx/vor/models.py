

from django.contrib.gis.db import models

"""
@todo: This lot needs to mix in

"""


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
	geom = models.PointField(srid=CustomSRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	

