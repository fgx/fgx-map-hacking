
from django.contrib.gis.db import models

## @todo: pete grab the aircraft from the fg repos (code in local machine)

##http://www.faa.gov/air_traffic/publications/atpubs/ATC/AppdxA.html#AppdxA.html.1

class EngineType(models.Model):
	engine_pk  models.IntegerField(primary_key=True) 
	eng = models.CharField(max_length=1, unique=True, db_index=True)
	engine = models.CharField(max_length=10, unique=True, db_index=True)
	
class WeightClass(models.Model):
	


class Manuf(models.Model):
	class Meta:
		db_table = "aero_manuf"
	
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
			
			