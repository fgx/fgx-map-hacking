"""The application's model objects"""




from fgx.model.meta import Sess, Base

## Load all the models here, so 'paster setup-app foo.ini' can create tables
from fgx.model.navdata import *
from fgx.model.users import *
from fgx.model.mpnet import *

def init_model(engines):
    """Call me before using any of the tables or classes in the model"""
    Sess.navdata.configure(bind=engines.navdata)
    Sess.users.configure(bind=engines.users)
    Sess.mpnet.configure(bind=engines.mpnet)
   


