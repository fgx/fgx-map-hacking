


from django.contrib.gis.db import models

from settings import FGX_SRID

##=======================================================
class Fix(models.Model):
	
	class Meta:
		db_table = "fix"
		verbose_name = "fix"
		verbose_name_plural = "fix"
	
	fix_pk = models.AutoField( primary_key=True)
	fix = models.CharField(max_length=10, db_index=True)	
	geom = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Fix: %s>" % (self.fix)
	
	
	def dic(self):
		
		return dict(
				fix = self.fix,
				fix_pk = self.fix_pk,
				lat = self.geom.coords[0], 
				lon = self.geom.coords[1]
			
		)
	
