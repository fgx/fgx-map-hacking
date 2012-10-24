
## First attemp at Flask + sqlAlchemy + Postgis

from fgx import db
from geoalchemy import GeometryColumn, Point, Geometry, GeometryDDL

from settings import FGX_SRID




##=======================================================
class Dme(models.Model):
	
	class Meta:
		db_table = "dme"
	
	dme_pk = db.Column(db.Integer, primary_key=True)
	ident = db.Column(db.String(4, db_index=True)
	name = db.Column(db.String(40, db_index=True)
	subtype = db.Column(db.String(10)
	elevation_m = db.Column(db.Integer())
	freq_mhz = db.Column(db.String(10)
	range_km = db.Column(db.String(10)
	bias_km = db.Column(db.Integer())
	wkb_geometry = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	

	
	
	
## TODO
class Fix(db.Model):
	
	__tablename__ = 'fix'
	
	fix_pk = db.Column(db.Integer, primary_key=True)
	fix = db.Column(db.String(10), index=True)
	geometry = GeometryColumn(Point(2, srid=FGX_SRID))
   
GeometryDDL(Fix.__table__)


##=======================================================
class Ndb(models.Model):
	
	class Meta:
		db_table = "ndb"
	
	ndb_pk = db.Column(db.Integer, primary_key=True)
	
	ident = db.Column(db.String(10), db_index=True)
	name = db.Column(db.String(50), db_index=True)
	freq_khz = db.Column(db.String(6))
	
	elevation_ft = db.Column(db.Integer())
	elevation_m = db.Column(db.Integer())
	range_nm = db.Column(db.Integer())
	range_m = db.Column(db.Integer())
	
	wkb_geometry = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Ndb: %s>" % (self.ident)
		
		

##=======================================================
class Vor(db.Model):
	
	__tablename__ = "vor"
	
	vor_pk = db.Column(db.Integer, primary_key=True)
	
	ident = db.Column(db.String(10, db_index=True)
	name = db.Column(db.String(50, db_index=True)
	freq_mhz = db.Column(db.String(6)
	
	elevation_ft = db.Column(db.Integer())
	elevation_m = db.Column(db.Integer())
	range_nm = db.Column(db.Integer())
	range_m = db.Column(db.Integer())
	
	# TODO What is this exactly ?
	variation = db.Column(db.String(10)
	
	wkb_geometry = models.PointField(srid=FGX_SRID)
	objects = models.GeoManager()

	def __repr__(self):
		return "<Ndb: %s>" % (self.ident)