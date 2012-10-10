"""The application's model objects"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, Numeric, String
from geoalchemy import GeometryColumn, Polygon, Point, GeometryDDL

from fgxmap.model.meta import Session, Base


def init_model(engine):
	"""Call me before using any of the tables or classes in the model"""
	Session.configure(bind=engine)



##=======================================================
class Airport(Base):
	__tablename__ = "airport"
	
	apt_id = Column(Integer, primary_key=True)
	apt_icao = Column(String(6), nullable=False, index=True)
	apt_name = Column(String(100), nullable=False, index=True)
	elevation = Column(String(30), nullable=False)
	geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Airport: %s>" % (self.icao)
	
GeometryDDL(Airport.__table__)



##=======================================================
class Dme(Base):
	__tablename__ = "dme"
	
	dme_id = Column(Integer, primary_key=True)
	ident = Column(String(4), nullable=False, index=True)
	name = Column(String(40), nullable=False, index=True)
	subtype = Column(String(10), nullable=True)
	elevation_m = Column(Integer(), nullable=True)
	freq_mhz = Column(String(10), nullable=True)
	range_km = Column(String(10), nullable=True)
	bias_km = Column(Numeric(precision=2, scale=None, as_decimal=True), nullable=True)
	geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Dme: %s>" % (self.icao)
	
GeometryDDL(Dme.__table__)



##=======================================================
class Fix(Base):
	__tablename__ = "fix"
	
	fix_id = Column(Integer, primary_key=True)
	fix_name = Column(String(10), nullable=False, index=True)
	geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Fix: %s>" % (self.icao)
	
GeometryDDL(Fix.__table__)



##=======================================================
class Runway(Base):
	__tablename__ = "runway"
	
	rwy_id = Column(Integer, primary_key=True)
	apt_icao = Column(String(10), nullable=False, index=True)
	rwy = Column(String(10), nullable=False, index=True)
	length = Column(String(30), nullable=False)
	geometry = GeometryColumn(Polygon(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Runway: %s-%s>" % (self.icao, self.rwy_id)
	
GeometryDDL(Runway.__table__)





##=======================================================
class Threshold(Base):
	__tablename__ = "threshold"

	thresh_id = Column(Integer(), primary_key=True)
	rwy_id = Column(Integer(), index=True)
	apt_icao = Column(String(10), nullable=False, index=True)
	rwy = Column(String(10), nullable=False, index=True)
	
	overrun_id = Column(Integer(), index=True, nullable=True)
	marking_id = Column(Integer(), index=True, nullable=True)
	appr_light_id = Column(Integer(), index=True, nullable=True)
	tdz_light_id = Column(Integer(), index=True, nullable=True)
	
	geometry = GeometryColumn(Polygon(), srid=3857, spatial_index=True)
	
	def __repr__(self):
		return "<Threshold: %s-%s>" % (self.apt_icao, self.rwy)
	
GeometryDDL(Threshold.__table__)




