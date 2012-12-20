##@package fgx.model.meta 
# @brief SQLAlchemy Metadata and Session objects
#
# The meta is the typical way to access sqlAlchemy sessions and the isntances within.
# @example from fgx.model import meta
#         

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


__all__ = ['Base', 'Sess']

##@brief A class to hold the database connections, sessions and metadata; currently three.....
class DbConnectionsContainer():
	
	## Constructor
	def __init__(self):
		
		## postgis database with navigation data
		self.navdata = None
		
		## users info and profile, shared data etc
		self.users = None
		
		## tracker and multiplayer
		self.mpnet = None
		
		
		
##@brief The sqlalchemy database Sessions/connecctions
#
# @see fgx.model.init_model()
Sess = DbConnectionsContainer()
Sess.navdata = scoped_session(sessionmaker())
Sess.users = scoped_session(sessionmaker())
Sess.mpnet = scoped_session(sessionmaker())


## The declarative Base for ORM access
Base = DbConnectionsContainer()
Base.navdata = declarative_base()
Base.users = declarative_base()


Base.mpnet = declarative_base()






#########################################################
## pete's data helpers
#########################################################
def select_sql(cmap):
	lst = cmap.replace("\t", "").strip().replace("\n", "").split(" ")
	arrc = [ s.strip() for s in lst]
	cols = []
	sqls = []
	for colr in arrc:
		col = colr.strip()
		if len(col) > 0:
			if col.find(" as ") > -1:
				p = col.split(" ")
				pp = []
				for pl in p:
					if len(pl) > 0:
						pp.append(pl)
				cols.append(pp[2])
				sqls.append(col)
			else:
				cols.append(col)
				sqls.append(col)
	sql = 'select ' + ", ".join(sqls)
	sql += " " # ta
	return sql, cols
	
def query_to_dic(resultsObj, cols):
	return_list = []
	for r in resultsObj:
		dic = {}
		for c in cols:
			dic[c] = r[c]
		return_list.append(dic)
	return return_list	

	