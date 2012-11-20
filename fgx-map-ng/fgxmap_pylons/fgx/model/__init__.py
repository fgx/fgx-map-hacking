"""The application's model objects"""


from sqlalchemy import  Integer, String, Date, DateTime
from geoalchemy import  Column, GeometryColumn, GeometryDDL, Point, Polygon, MultiPoint
from geoalchemy.postgis import PGComparator
from shapely import wkb;

from fgx.model.meta import Sess, Base


def init_model(engines):
    """Call me before using any of the tables or classes in the model"""
    Sess.data.configure(bind=engines.data)
    Sess.secure.configure(bind=engines.secure)
    Sess.mp.configure(bind=engines.mp)
   
FGX_SRID = 3857

