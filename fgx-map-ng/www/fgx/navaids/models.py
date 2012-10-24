
## First attemp at Flask + sqlAlchemy + Postgis


from geoalchemy import GeometryColumn, Point, Geometry, GeometryDDL
from geoalchemy.postgis import PGComparator

from fgx import db
from settings import FGX_SRID




##=======================================================
class Dme(db.Model):
	
	__tablename__ = "dme"
	
	dme_pk = db.Column(db.Integer(), primary_key=True)
	ident = db.Column(db.String(4), index=True)
	name = db.Column(db.String(40), index=True)
	subtype = db.Column(db.String(10))
	elevation_m = db.Column(db.Integer())
	freq_mhz = db.Column(db.String(10))
	range_km = db.Column(db.String(10))
	bias_km = db.Column(db.Integer())
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	
GeometryDDL(Dme.__table__)
	
	
##=======================================================	
class Fix(db.Model):
	
	__tablename__ = 'fix'
	
	fix_pk = db.Column(db.Integer(), primary_key=True)
	fix = db.Column(db.String(10), index=True)
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

GeometryDDL(Fix.__table__)


##=======================================================
class Ndb(db.Model):
	
	__tablename__ = "ndb"
	
	ndb_pk = db.Column(db.Integer(), primary_key=True)
	
	ident = db.Column(db.String(10), index=True)
	name = db.Column(db.String(50), index=True)
	freq_khz = db.Column(db.String(6))
	
	elevation_ft = db.Column(db.Integer())
	elevation_m = db.Column(db.Integer())
	range_nm = db.Column(db.Integer())
	range_m = db.Column(db.Integer())
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Ndb: %s>" % (self.ident)
		
GeometryDDL(Ndb.__table__)		

##=======================================================
class Vor(db.Model):
	
	__tablename__ = "vor"
	
	vor_pk = db.Column(db.Integer, primary_key=True)
	
	ident = db.Column(db.String(10), index=True)
	name = db.Column(db.String(50), index=True)
	freq_mhz = db.Column(db.String(6))
	
	elevation_ft = db.Column(db.Integer())
	elevation_m = db.Column(db.Integer())
	range_nm = db.Column(db.Integer())
	range_m = db.Column(db.Integer())
	
	# TODO What is this exactly ?
	variation = db.Column(db.String(10))
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Vor: %s>" % (self.ident)
		
GeometryDDL(Vor.__table__)

