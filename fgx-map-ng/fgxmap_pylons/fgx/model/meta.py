"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Base', 'Session']

# SQLAlchemy session manager. Updated by model.init_model()
## Need this is object
class SessionHolder(object):
	pass

Sess = SessionHolder()
Sess.data = scoped_session(sessionmaker())
Sess.secure = scoped_session(sessionmaker())
Sess.mp = scoped_session(sessionmaker())
#Sess.tracker = scoped_session(sessionmaker())


# The declarative Base
class BaseContainer(object):
	pass
Base = BaseContainer()
Base.data = declarative_base()
Base.secure = declarative_base()
Base.mp = declarative_base()
#Base.tracker = declarative_base()
#Base.contrib = declarative_base()






#########################################################
## pete's data helpers
#########################################################
def select_sql(cmap):
	lst = cmap.replace("\t", "").replace("\n", "").split(" ")
	arrc = [ s.strip() for s in lst]
	cols = []
	sqls = []
	for col in arrc:
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

def UMM_results_to_dic(arr, results):
	ret = []
	for r in results:
		d = {}
		for idx in range(0, len(arr) ):
			
			ki = arr[idx].split(".")[1] if arr[idx].find(".") > 1 else arr[idx]
			vari = r[idx]
			
			if isinstance(vari, datetime.datetime):
				d[ki] = vari.strftime("%Y-%m-%d %H:%M:%S")
				
			elif isinstance(vari, datetime.date):
				d[ki] = vari.strftime("%Y-%m-%d")# %H:%M:%S")
			
			elif isinstance(vari, float) or isinstance(vari, int) or isinstance(vari, long):
				d[ki] = vari
				#print "float, int", vari
			
			elif vari == None:
				d[ki] = None
				
			#elif isinstance(vari, str):
			#	d[ki] = vari
				#d[ki] = "#%s" % r[idx]
				#print "XX", type(vari), vari
			else:
				try:
					sss = vari.decode("ascii")
				except UnicodeDecodeError:
					safeS = ""
					for cIdx in  range(0, len(vari)):
						singleS = vari[cIdx]
						if ord(singleS) < 128:
							safeS += singleS
						else:
							safeS += "#@~"
					sss = safeS
					#print "FUCKER=", vari, type(vari)
				#else:
				#	print "WTF=", vari, type(vari)
				d[ki] = sss
		ret.append(d)
	return ret
