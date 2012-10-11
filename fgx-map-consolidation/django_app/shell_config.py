
## Configuration for shell

print "SHELL CONF"


import os
import sys

## Append some of the parent paths
print sys.path

sys.path.append( os.path.abspath(  os.path.dirname(__file__)   ) )
#sys.path.append( os.path.abspath(  os.path.dirname(__file__) + "/../fgx_www"  ) )
#sys.path.append( os.path.abspath(  os.path.dirname(__file__) + "/../libs"  ) )


## Load Django enviroment
"""
from django.core.management import setup_environ
import settings
setup_environ(settings)
"""
