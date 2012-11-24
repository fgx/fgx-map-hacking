
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
		print "FGxOO INIT>>", dic.keys()
		
		for k in dic:
			WhatAmIm = dic[k]
			#print "READ=", k, dic[k]
			if WhatAmIm == None:
				print "SET WHAT??"
				self.__dict__[k] = None
			else:	
				WhatAmIm = dic[k]
				if isinstance(WhatAmIm, str):
					self.__dict__[k] = WhatAmIm
					print "\tSET = str", k #, WhatAmIm
				
				elif isinstance(WhatAmIm, unicode):
					self.__dict__[k] = WhatAmIm
					print "\tSET = uni", k #, WhatAmIm
				
				elif isinstance(WhatAmIm, dict):
					self.__dict__[k] = FGxOO(WhatAmIm)
					print "\tSET = FGx_OO!", k #, WhatAmIm
				
				else:
					print "\tSET = WTF", k, WhatAmIm
					self.__dict__[k] = WhatAmIm
					
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
	