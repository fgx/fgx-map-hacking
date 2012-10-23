
## First attemp at Flask + sqlAlchemy + Postgis

from fgx import db


## TODO
class Fix(db.Model):
	
	__tablename__ = 'fix222'
	
	fix_pk = db.Column(db.Integer, primary_key=True)
	fix = db.Column(db.String)
    geometry = db.GeometryColumn(Point(2))
    