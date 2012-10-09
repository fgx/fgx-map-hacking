
import yaml

from fgx import app_global as G 


## Return a list of projects from the config
def projects():
	
	dic = yaml.load( G.read_file("/config/projects.yaml") )
	return dic

	