##@package fgx.model
# @brief The database and model configuration is different from the default pylons app 
#        bacause it contains more than one db connection.






from fgx.model.meta import Sess, Base


from fgx.model.navdata import *
from fgx.model.users import *
from fgx.model.mpnet import *
		

##@brief Initialises and binds engines to sessions
# @param engines The engines created in config.environment.load_environment() and instance of model.meta.DbConnectionsContainer
def init_model(engines):
    Sess.navdata.configure(bind=engines.navdata)
    Sess.users.configure(bind=engines.users)
    Sess.mpnet.configure(bind=engines.mpnet)
   


