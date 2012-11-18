

print "Initialising Shell Config .."

import os, sys

ROOT_PATH = os.path.abspath(  os.path.join(os.path.dirname(__file__)))  

if not ROOT_PATH in sys.path:
	sys.path.insert(0, ROOT_PATH)
	print "  > Appended path ", ROOT_PATH
	

from paste.deploy import appconfig
appConfig = appconfig('config:local.ini', relative_to=ROOT_PATH)


from fgx.config.environment import load_environment
config = load_environment( appConfig.global_conf, appConfig.local_conf, False)

	