
from settings import ROOT

## Reads file from project relative to ROOT
def read_file(path):
	f = open(ROOT + path, "r")
	s = f.read()
	f.close()
	return s
	
## Reads file from project relative to ROOT
def write_file(path, contents):
	f = open(ROOT + path, "w")
	s = f.write(contents)
	f.close()
	return 
	