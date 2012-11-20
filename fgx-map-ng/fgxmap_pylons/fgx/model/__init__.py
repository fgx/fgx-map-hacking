"""The application's model objects"""




from fgx.model.meta import Sess, Base
from fgx.model.data import *
from fgx.model.secure import *

def init_model(engines):
    """Call me before using any of the tables or classes in the model"""
    Sess.data.configure(bind=engines.data)
    Sess.secure.configure(bind=engines.secure)
    Sess.mp.configure(bind=engines.mp)
   


