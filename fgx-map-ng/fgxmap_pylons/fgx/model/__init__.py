"""The application's model objects"""




from fgx.model.meta import Sess, Base

## Load all the models here, so 'paster setup-app foo.ini' can create tables
from fgx.model.data import *
from fgx.model.secure import *
from fgx.model.mpnet import *

def init_model(engines):
    """Call me before using any of the tables or classes in the model"""
    Sess.data.configure(bind=engines.data)
    Sess.secure.configure(bind=engines.secure)
    Sess.mpnet.configure(bind=engines.mpnet)
   


