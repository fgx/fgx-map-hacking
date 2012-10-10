"""The application's model objects"""

from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from geoalchemy import GeometryColumn, Polygon, Point, GeometryDDL

from fgxmap.model.meta import Session, Base


def init_model(engine):
	"""Call me before using any of the tables or classes in the model"""
	Session.configure(bind=engine)

	"""
	self.cur.execute("DROP TABLE IF EXISTS runways;")
		self.cur.execute("CREATE TABLE runways (ogc_fid serial PRIMARY KEY, \
					icao varchar, \
					rwy_id varchar, \
					rwy_id_end varchar, \
					rwy_width varchar, \
					rwy_length_meters varchar, \
					rwy_length_feet varchar, \
					wkb_geometry geometry(Polygon,4326));")

	"""


##=======================================================
class Airport(Base):
	__tablename__ = "airports"
	
	ogc_fid = Column(Integer, primary_key=True)
	icao = Column(String(6), nullable=False, index=True)
	name = Column(String(100), nullable=False, index=True)
	elevation = Column(String(30), nullable=False)
	wkb_geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Airport: %s>" % (self.icao)
	
GeometryDDL(Airport.__table__)



##=======================================================
class Fix(Base):
	__tablename__ = "fix"
	
	ogc_fid = Column(Integer, primary_key=True)
	fix_name = Column(String(100), nullable=False, index=True)
	wkb_geometry = GeometryColumn(Point(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Fix: %s>" % (self.icao)
	
GeometryDDL(Fix.__table__)



##=======================================================
class Runway(Base):
	__tablename__ = "runways"
	
	ogc_fid = Column(Integer, primary_key=True)
	icao = Column(String(10), nullable=False, index=True)
	rwy_id = Column(String(10), nullable=False, index=True)
	length = Column(String(30), nullable=False)
	wkb_geometry = GeometryColumn(Polygon(), srid=3857, spatial_index=True)

	def __repr__(self):
		return "<Runway: %s-%s>" % (self.icao, self.rwy_id)
	
GeometryDDL(Runway.__table__)

