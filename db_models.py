#!/usr/bin/env python

import os
import yaml
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

from geoalchemy import *
from geoalchemy.postgis import PGComparator

FGX_SRID = 3857

here = os.path.abspath( os.path.dirname(__file__) ) + "/"
f = open( here + "db_conf.yaml")
data = yaml.load(f.read())['database']
f.close()
print data

connection_str = "postgresql+psycopg2://%s:%s@localhost/%s" % (data['user'], data['password'], data['database'])

engine = create_engine(connection_str)
DeclarativeBase = declarative_base()
metadata = DeclarativeBase.metadata
metadata.bind = engine

##=======================================================
class Airport(DeclarativeBase):
	
	__tablename__ = "airport"
	
	dme_pk = Column(Integer(), primary_key=True)
	ident = Column(String(4), index=True)
	name = Column(String(40), index=True)
	subtype = Column(String(10))
	elevation_m = Column(Integer())
	freq_mhz = Column(String(10))
	range_km = Column(String(10))
	bias_km = Column(Integer())
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	
GeometryDDL(Airport.__table__)


##=======================================================
class Dme(DeclarativeBase):
	
	__tablename__ = "dme"
	
	dme_pk = Column(Integer(), primary_key=True)
	ident = Column(String(4), index=True)
	name = Column(String(40), index=True)
	subtype = Column(String(10))
	elevation_m = Column(Integer())
	freq_mhz = Column(String(10))
	range_km = Column(String(10))
	bias_km = Column(Integer())
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	
GeometryDDL(Dme.__table__)
	
	
	
##=======================================================	
class Fix(DeclarativeBase):
	
	__tablename__ = 'fix'
	
	fix_pk = Column(Integer(), primary_key=True)
	fix = Column(String(10), index=True, nullable=False)
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)
	
GeometryDDL(Fix.__table__)



##=======================================================
class Ndb(DeclarativeBase):
	
	__tablename__ = "ndb"
	
	ndb_pk = Column(Integer(), primary_key=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq_khz = Column(String(6))
	
	elevation_ft = Column(Integer())
	elevation_m = Column(Integer())
	range_nm = Column(Integer())
	range_m = Column(Integer())
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Ndb: %s>" % (self.ident)
		
GeometryDDL(Ndb.__table__)		



##=======================================================
class Vor(DeclarativeBase):
	
	__tablename__ = "vor"
	
	vor_pk = Column(Integer, primary_key=True)
	
	ident = Column(String(10), index=True)
	name = Column(String(50), index=True)
	freq_mhz = Column(String(6))
	
	elevation_ft = Column(Integer())
	elevation_m = Column(Integer())
	range_nm = Column(Integer())
	range_m = Column(Integer())
	
	# TODO What is this exactly ?
	variation = Column(String(10))
	
	wkb_geometry = GeometryColumn(Point(2, srid=FGX_SRID), comparator=PGComparator)

	def __repr__(self):
		return "<Vor: %s>" % (self.ident)
		
GeometryDDL(Vor.__table__)



