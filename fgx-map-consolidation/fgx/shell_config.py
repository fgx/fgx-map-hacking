## Configuration for shell



import os
import sys


sys.path.append( os.path.abspath(  os.path.dirname(__file__)  + "/fgxmap"  ) )
#sys.path.append( os.path.abspath(  os.path.dirname(__file__) + "/../fgx_www"  ) )
#sys.path.append( os.path.abspath(  os.path.dirname(__file__) + "/../libs"  ) )

TEMP_DIR =  os.path.abspath( os.path.join(os.path.dirname(__file__), "../_temp/")) 
CACHE_DIR =  os.path.abspath( os.path.join(os.path.dirname(__file__), "../_cache/")) 


#print "TEMP_DIR=", TEMP_DIR

## Load Django enviroment
from django.core.management import setup_environ
import settings
setup_environ(settings)

