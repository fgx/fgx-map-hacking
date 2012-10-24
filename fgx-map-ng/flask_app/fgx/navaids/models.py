
## First attemp at Flask + sqlAlchemy + Postgis

from fgx import db
from geoalchemy import GeometryColumn, Point, Geometry, GeometryDDL

from settings import FGX_SRID

## TODO
class Fix2(db.Model):
	
	__tablename__ = 'fix2'
	
	fix_pk = db.Column(db.Integer, primary_key=True)
	fix = db.Column(db.String(10), index=True)
	geometry = GeometryColumn(Point(2, srid=FGX_SRID))
   
GeometryDDL(Fix2.__table__)
