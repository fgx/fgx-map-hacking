##@package fgx.model.navdata 
# @brief Users data and profile models
#


from sqlalchemy import  Integer, String, Date, DateTime, Column
from fgx.model.meta import Sess, Base

##=======================================================
class BookMark(Base.users):
	
	__tablename__ = "bookmark"
	
	bookmark_id = Column(Integer(), primary_key=True) 
	
	name = Column(String(100), index=True)
	lat = Column(String(15))
	lon = Column(String(15))
	zoom = Column(Integer())
	



##=======================================================
class User(Base.users):
	
	__tablename__ = "user"
	
	user_id = Column(Integer, primary_key=True)
	
	email = Column(String(50), index=True, nullable=False)
	name = Column(String(50), index=True, nullable=False)
	callsign = Column(String(10), nullable=False)
	passwd = Column(String(100), nullable=False)
	
	## Security level.. idea atmo is 0 = disabled, 1 = Auth, 2 = Admin, 
	level = Column(Integer, nullable=False)
	
	created = Column(DateTime(), nullable=False)
	
	
##=======================================================
class UserLog(Base.users):
	
	__tablename__ = "user_log"
	
	log_id = Column(Integer, primary_key=True)
	user_id = Column(Integer, nullable=False)
	
	event = Column(String(50), index=True, nullable=False)
	log = Column(String(255), nullable=False)
	ts = Column(DateTime(), nullable=False)
	
	
	