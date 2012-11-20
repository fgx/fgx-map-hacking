



##=======================================================
class BookMark(Base.secure):
	
	__tablename__ = "bookmark"
	
	bookmark_pk = Column(Integer(), primary_key=True) 
	
	name = Column(String(100), index=True)
	lat = Column(String(15))
	lon = Column(String(15))
	zoom = Column(Integer())



##=======================================================
class User(Base.secure):
	
	__tablename__ = "user"
	
	user_pk = Column(Integer, primary_key=True)
	
	email = Column(String(50), index=True, nullable=False)
	name = Column(String(50), index=True, nullable=False)
	callsign = Column(String(10), nullable=False)
	passwd = Column(String(100), nullable=False)
	
	## Security level.. idea atmo is 0 = disabled, 1 = Auth, 2 = Admin, 
	level = Column(Integer, nullable=False)
	
	created = Column(DateTime(), nullable=False)
	
	