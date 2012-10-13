"""
@brief Loads teh Djanjo enviroment for a shell
"""

import os
import sys

## At present the PROJ_ROOT is the repos root


sys.path.append( os.path.abspath(  os.path.dirname(__file__)  + "/fgxmap"  ) )
#sys.path.append( os.path.abspath(  os.path.dirname(__file__) + "/../fgx_www"  ) )
#sys.path.append( os.path.abspath(  os.path.dirname(__file__) + "/../libs"  ) )

TEMP_DIR =  os.path.abspath( os.path.join(os.path.dirname(__file__), "../_temp/")) 
CACHE_DIR =  os.path.abspath( os.path.join(os.path.dirname(__file__), "../_cache/")) 


""" Checks if the shell enviroment is sane """
def sanity_check():
	print "Sanity Check"
	
	if os.path.exists(TEMP_DIR):
		print "TEMP DIR NTO EXIST"
		Throw_trntrum
	
	return False
	


#print "TEMP_DIR=", TEMP_DIR

## Load Django enviroment
from django.core.management import setup_environ
import settings
setup_environ(settings)

