

from fgx import db

## We need to load add the files with models here so their registeres with sqlalchemy

from fgx.navaids import models

def create_all():
	
	print "Create All"
	db.create_all()
	
	
def drop_all():
	
	print "Drop All"
	db.drop_all()
	