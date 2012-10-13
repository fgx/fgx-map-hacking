"""
@brief Loads teh Djanjo enviroment for a shell
"""

import os
import sys

sys.path.append( os.path.abspath(  os.path.dirname(__file__)  + "/../fgx"  ) )

import settings

""" Checks if the shell enviroment is sane """
def sanity_check():
	print "> Shell Sanity Check: "
	
	print "  > Check Temp Dir: ",
	if os.path.exists(settings.TEMP_DIR):
		print "TEMP DIR NTO EXIST"
		print "Fail"
		Throw_trntrum
	else:
		print "Ok = " + settings.TEMP_DIR
	
	print "  > Sanity OK"
	return True
	
sanity_check()



###############################################
## Load Django enviroment
print "> Setup Django Shell: ",
from django.core.management import setup_environ

setup_environ(settings)
print "Succesful"

