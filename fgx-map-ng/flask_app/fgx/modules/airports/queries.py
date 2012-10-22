
import datetime
import re

from fgx import db  #, cache


##==============================================================================
### Airports Search
def airports(apt_icao=None, apt_name=None, icao_only=True):
	
	ex_icao = re.compile("[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]") # [a-zA-Z]{4} ? 
	
	
	# down and dirty way for now.. raw code to see if pattern emerges..
	sql = "select rtrim(apt.apt_icao), rtrim(apt.apt_name) "
	sql += "from apt "
	
	
	#params = {}
	if apt_icao != None:
		sql += " where apt.apt_icao ilike '" + apt_icao.upper() + "%' " #todo placeholder
	
	elif apt_name != None:
		sql += " where apt.apt_name ilike '%" + apt_name + "%' " #todo placeholder
		
	sql += "limit 500 "
	results = db.session.execute(sql).fetchall()
	
	ret = []
	for row in results:
		if ex_icao.match(row[0]):

			ret.append(	{'apt_icao': row[0], 'apt_name': row[1] }	)

	return ret	


##==============================================================================
#@cache.cached(timeout=20, key_prefix="airports_count")
def airports_count(apt_icao=None):

	
	sql = "select count(*) from apt "
	results = db.session.execute(sql).fetchall()
	#print "CALL", sql
	return results[0][0]
	
	
	
#==============================================================================
def airport(apt_icao):

	sql = "select rtrim(apt.apt_icao) as apt_icao, rtrim(apt.apt_name) as apt_name "
	sql += "from apt "
	sql += " where apt.apt_icao = :apt_icao "
	
	cols = ["apt_icao", "apt_name"]
	
	results = db.session.query(*cols
						).from_statement(sql
						).params(apt_icao=apt_icao).all()	
	if len(results) == 0:
		return None
		
	#dic = {}
	#for idx, col in enumerate(cols):
	#'	dic[col] = results[0][idx]
	
	return dict(zip(cols, results[0])) 
	
#==============================================================================	
def atc(apt_iaco):
	sql = "select rtrim(atcfreq.apt_icao) as apt_icao, rtrim(atcfreq.atc_type) as atc_type, "
	sql = "rtrim(atcfreq.freq_name) as freq_name, rtrim(atcfreq.freq_mhz) as freq_mhz, "
	sql += "from atcfreq "
	sql += " where atcfreq.apt_icao = :apt_icao "
	cols = ["apt_icao", "atc_type", "freq_name", "freq_mhz"]
	results = db.session.query(*cols
						).from_statement(sql
						).params(apt_icao=apt_icao).all()
	print results, type(results)	
	"""	
	sql = "select rtrim(apt.apt_icao), rtrim(apt.apt_name) "
	sql += "from apt "
	sql += " where apt.apt_icao = %(apt_icao)s' "
	
	results = db.session.execute(sql, params={apt_icao: apt_icao}).fetchall()
	"""
	if len(results) == 0:
		return None
	dic = {}
	for idx, col in enumerate(cols):
		dic[col] = col[idx]
	#ret = {}
	return dic
	
	
	
	
	
	
	
	
	
	
	
##==============================================================================
## return aptdat
def aptdat_tables():
	
	sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'";
	
	ret = []
	for row in db.session.execute(sql).fetchall():
		ret.append(row[0])
		
	return ret
	
	return "YS"
	