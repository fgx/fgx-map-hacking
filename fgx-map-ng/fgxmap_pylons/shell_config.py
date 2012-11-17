
print "Shelll Config"

import os, sys

ROOT_PATH = os.path.abspath(  os.path.join(os.path.dirname(__file__)))  

if not ROOT_PATH in sys.path:
	sys.path.insert(0, ROOT_PATH)
	print "  > Appended path ", ROOT_PATH
	

from paste.deploy import appconfig

#ini = xpath + '/development.ini'

appConfig = appconfig('config:local.ini', relative_to=ROOT_PATH)

#import os, sys
#here_path = os.path.abspath(  os.path.dirname(__file__) )  
#x_path =   os.path.abspath(os.path.join(here_path, "fgxmap_pylons"))
#if not x_path in sys.path:
#	#sys.path.append(x_path)
#	#print "  > Appended path ", x_path
	
#print here_path, x_path
#ini = x_path + '/development.ini'
#print "ini=", ini
#conf = appconfig('config:' + "development.ini", relative_to=x_path)

from fgx.config.environment import load_environment
config = load_environment( appConfig.global_conf, appConfig.local_conf, False)

def temp_dir():
	return config['temp_dir']
	