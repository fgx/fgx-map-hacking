
## First attemp at Flask + sqlAlchemy + Postgis

from fgx import db



class Fix(db.Model):
	
	__tablename__ = 'fix'
	
    fix_pk = db.Column(db.Integer, primary_key=True)
    fix = db.Column(db.String)
    
    