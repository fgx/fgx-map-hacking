

print "Initialising Shell Config .."

import os, sys

ROOT_PATH = os.path.abspath(  os.path.join(os.path.dirname(__file__)))  

if not ROOT_PATH in sys.path:
	sys.path.insert(0, ROOT_PATH)
	print "  > Appended path ", ROOT_PATH
	

from paste.deploy import appconfig
from fgx.config.environment import load_environment

config = None

def configure(ini_file):
	global config
	ini_path = os.path.abspath(os.path.join(os.path.dirname(__file__))) + "/" + ini_file
	if not os.path.exists( ini_path ):
		print "FATAL: Ini file '%s' does not exist" % ini_path
		sys.exit(1)
		
	appConfig = appconfig('config:%s' % ini_file, relative_to=ROOT_PATH)
	config = load_environment( appConfig.global_conf, appConfig.local_conf, False)

	