
import sys
import os
import yaml
import psycopg2

# database connection
global CONN
CONN = None


global DB
DB = None

HERE = os.path.dirname(__file__)

class FGxOO:

	def __init__(self, dic):
		#print "FGxOO INIT>>", dic, type(dic)
		
		for k in dic:
			WhatAmIm = dic[k]
			#print "READ=", k, dic[k]
			if WhatAmIm == None:
				#print "SET WHAT??"
				self.__dict__[k] = None
			else:	
				WhatAmIm = dic[k]
				#if isinstance(WhatAmIm, str):
				#	self.__dict__[k] = WhatAmIm
				#	#print "\tSET = str", k #, WhatAmIm
				
				#elif isinstance(WhatAmIm, unicode):
				#	self.__dict__[k] = WhatAmIm
					#print "\tSET = uni", k #, WhatAmIm
				if isinstance(WhatAmIm, dict):
					self.__dict__[k] = FGxOO(WhatAmIm)
					#ddprint "\tSET = FGx_OO!", k #, WhatAmIm
				
				elif isinstance(WhatAmIm, list):
						
						#print "\tSET = LIST", k, type(WhatAmIm), WhatAmIm
						self.__dict__[k] = [FGxOO(d) for d in WhatAmIm]
						
				else:	
					#print "\t### SET=unknows",  k, type(WhatAmIm), WhatAmIm
					self.__dict__[k] = WhatAmIm

def init_db(db_yaml_path):
	
	ob = load_yaml(db_yaml_path, as_object=True)
	#ob = FGxOO(conf)

	conn_str = "dbname=%s user=%s password=%s dbname=%s" % (
			ob.database, ob.user, ob.password, ob.database )
	if ob.host :
		conn_str += " host=%s" % ob.host
		
	print "Connect: ", conn_str
	
	global CONN
	global DB
	CONN = psycopg2.connect(conn_str)
	DB = CONN.cursor()


def load_yaml(file_path, as_object=False):
	#print "load_yaml", file_path
	f = open(file_path, "r")
	data_dict = yaml.load(f.read())
	f.close()
	if as_object:
		return FGxOO(data_dict)
	return data_dict