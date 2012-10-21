
from django.db import connection, transaction

cursor = connection.cursor()
    

def fix(search=None, ident=None):
	
	## list columns seperated by spaces
	cols = "fix lat lon".split()
	
	sql = "select fix_pk, fix from fix where fix like '%%%s%%';" % search
	
	
	cursor.execute(sql)
	
	rows = cursor.fetchall()
	
	return rows