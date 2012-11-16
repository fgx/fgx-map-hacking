
from django.db import connection, transaction

cursor = connection.cursor()
    
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
    
def fix(search=None, ident=None):
	
	## list columns seperated by spaces
	cols = "fix lat lon".split()
	
	#sql = "select fix_pk, fix from fix where fix like '%s';" 
	
	
	cursor.execute("select fix_pk, fix from fix where fix like %s;" , ['%' + search + '%'])
	
	rows = dictfetchall(cursor)
	
	#for row in  cursor.fetchall():
	#	rows.append(row)
	return rows