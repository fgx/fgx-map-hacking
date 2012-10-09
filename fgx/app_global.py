## 
# @file app_global.py 
# @package fgx
# Application Globals 
# 
# Normaly used as import app_global as G

import os.path
import yaml

## @var The absolute path to project root
PROJECT_ROOT =  os.path.abspath( os.path.join(os.path.dirname(__file__), "../"))
#print PROJECT_ROOT


## List of apt-get packes to checkfor
# @todo pete to handle this
PACKAGES = """

python-yaml
python-simplejson
beautifulsoup4    
PyQt4

doxygen


mapnick

"""

## Reads file from project relative to PROJECT_ROOT
def read_file(path):
	f = open(PROJECT_ROOT + path)
	s = f.read()
	f.close()
	return s
	
