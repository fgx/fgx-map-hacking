
	
##=======================================================
class Aircraft(Base.aircraft):
	
	__tablename__ = "aircraft"
	
	aero_pk = Column(Integer(), primary_key=True) 
	#manufacturers = models.Remotekey()
	
	model = Column(String(10), unique=True, index=True)
	type_designator = Column(String(10))
	
	engines = Column(Integer())
	engine_type = Column(String(1))
	
	weight_class = Column(String(40))
	
	climb_rate_fpm = Column(String(40))
	descent_rate_fpm = Column(String(40))
	
	srs = Column(String(40))
	lahso = Column(Integer())
	



	
class EngineType(Base.aircraft):
	
	__tablename__ = "engine_type"
		
	engine_pk = Column(Integer(), primary_key=True)
	eng = Column(String(1), unique=True, index=True)
	engine = Column(String(10), unique=True, index=True)
	

	




class Manufacturer(Base.aircraft):
	
	__tablename__ = "manufacturer"
	
	manuf_pk = Column(Integer(), primary_key=True)
	manuf = Column(String(20), unique=True, index=True)
	
	"""
	manufacturer varchar, \
			model varchar, \
			type_designator varchar, \
			engines varchar, \
			weight_class varchar, \
			climb_rate varchar, \
			descent_rate varchar, \
			srs varchar, \
			LAHSO_group);
	"""
	




		




	


	
	