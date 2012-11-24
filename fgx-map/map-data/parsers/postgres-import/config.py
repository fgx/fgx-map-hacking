
import sys
import os
import yaml
import psycopg2

# database connection
global DB
DB = None

HERE = os.path.dirname(__file__)

class FGxOO:

	def __init__(self, dic):
		print "FGxOO Construct", dic.keys()
		
		for k in dic:
			print k, dic.keys()
			WhatAmIm = self.__dict__[k]
			if isinstance(WhatAmIm, str):
				self.__dict__[k] = WhatAmIm
				print "your a plain olde str", k, WhatAmIm
			
			elif isinstance(WhatAmIm, unicode):
				self.__dict__[k] = WhatAmIm
				print "tour unicide r", k, WhatAmIm
			"""
			if dic[k] == None:
				self.__dict__[k] = '' 
				print "set none=", k
			else:
				self.__dict__[k] = dic[k] #QtCore.QString( dic[k] )
				print "set=", k, dic[k]
				#self.__dict__[k] = dic[k] 
			"""

def init_db(db_yaml_path):
	
	conf = load_yaml(db_yaml_path)
	print "init_db", db_yaml_path #, conf
	ob = FGxOO(conf)
	#print ob.databases.keys()
	
	cred = ob.databases.aip
	print cred
	#conn_str = "dbname=%s user=%s password=%s dbname=%ss" % (ob.dat
	#connectstring = "dbname=" + conf['database'] + " user=" + conf['user'] + " password=" + conf['password']
	#if "host" in confMap:
	#	connectstring += " host=%s" % conf['host']
	
	conn = psycopg2.connect(connectstring)
	global DB
	DB = conn.cursor()


def load_yaml(file_path):
	#print "load_yaml", file_path
	f = open(file_path, "r")
	data = yaml.load(f.read())
	f.close()
	return data
	