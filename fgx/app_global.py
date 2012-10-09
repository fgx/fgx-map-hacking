## 
# @file app_global.py 
# Application Globals 
# 
# 
# \code 
# #Normaly used as 
# import app_global as G
# \endcode

import sys
import os
import yaml

## @var ROOT
# @brief The absolute path to project root
ROOT =  os.path.abspath( os.path.join(os.path.dirname(__file__), "../"))
#print ROOT


## List of apt-get packages to check for
# @todo pete to handle this
APT_PACKAGES = [
	"postgres-9.1",
	"postgis",
	"python-yaml",
	"python-qt4",
	"doxygen",
	"python-mapnik"
]

## List of python packages to check for
# @todo pete to handle this
PY_PACKAGES = [
	"BeautifulSoup4"    
	"psycopg2",
	"python-simplejson",
]


def check_sane():
	sane =  os.path.exists(ROOT + "/local_config.yaml")
	if not sane:
		print "ERROR: local_config.yaml is missing, Create with ./run_config.py -l"
		sys.exit(1)
	return True

## Reads file from project relative to ROOT
def read_file(path):
	f = open(ROOT + path, "r")
	s = f.read()
	f.close()
	return s
	
## Reads file from project relative to ROOT
def write_file(path, contents):
	f = open(ROOT + path, "w")
	s = f.write(contents)
	f.close()
	return 
	
