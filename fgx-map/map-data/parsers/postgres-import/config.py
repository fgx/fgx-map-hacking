
import os
import yaml

# database connection
global DB
DB = None

HERE = os.path.dirname(__file__)



def init(db_yaml_path):
	print "init", db_yaml_path
	creds = load_yaml(db_yaml_path)
	print creds
	
	connectstring = "dbname=" + confMap['database'] + " user=" + confMap['user'] + " password=" + confMap['password']
	if "host" in confMap:
		connectstring += " host=%s" % confMap['host']
	conn = psycopg2.connect(connectstring)
	cur = conn.cursor()


def load_yaml(file_path):
	print "load_yaml", file_path
	f = open(file_path, "r")
	data = yaml.load(f.read())
	f.close()
	return data
	