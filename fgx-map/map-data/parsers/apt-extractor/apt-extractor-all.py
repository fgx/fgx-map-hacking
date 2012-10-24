#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not remove this copyright notice.
#
# This is a helper script to extract airports from xplane apt.dat to single file
# Because it is a bad dumb script it will heat your machine, be careful ! NO WARRANTY !
#
# Scripts process 1000 airports (see maxcount value) and remain



import sys, csv, os, re, gc
from time import sleep
sys.path.append("/usr/local/lib/python/site-packages");

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
   print "Usage: python apt-extractor-all.py <apt.dat>"
   sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python apt-extractor-all.py <apt.dat>"
	sys.exit(0)
	
	
inputfile = sys.argv[1]
chunkin = 100 #how many airports per cycle in range of maxcount 
maxcount = 1000 #how many airports total with this task

gc.enable()

aptcounter = 0

def createlist():
	if not os.path.exists('airports_to_process.temp'):
		aptcounter = 0
		list = open(inputfile, 'r')
		listwriter = open('airports_to_process.temp', 'w')
		print "Looking for airports in .dat file ..."
		for aptline in list.readlines():
			if aptline.startswith("1  "):
				icaostring = aptline[15]+aptline[16]+aptline[17]+aptline[18]
				icaostringret = icaostring+'\n'
				listwriter.write(icaostringret)
				aptcounter += 1
		listwriter.close()
		print "Created list with "+str(aptcounter)+" airports (codes) in airports_to_process.temp"
	else:
		print "Aitports list to process already exists. Loading ..."
createlist()	

dir = "extracted"
dirs = ['A','B','C','D','E','F','G','H','J','I','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

if not os.path.exists(dir):
	os.makedirs(dir)
else:
	print "Directory 'extracted' already exist."

for i in dirs:
	path = dir+"/"+i
	if os.path.exists(path):
		print "Directory '"+path+"' already exist."
	else:
		os.makedirs(path)
		print "Creating directory '"+path


def aptbuff(aptfilename):
	allinalist = []
	counter = 0
	print "Starting to read the .dat file into buffy ..."
	aptreader = open(aptfilename, 'r')
	for line in aptreader.readlines():
		allinalist += [line]
		counter += 1
	print "Reading "+str(counter)+" lines"
	
	return allinalist
	
buffy = aptbuff(inputfile)

def listbuff():
	listlist = []
	counter = 0
	print "Reading the list to process into to other buffy ..."
	aptlistreader = open('airports_to_process.temp', 'r')
	for line in aptlistreader.readlines():
		listlist += [line]
		counter += 1
	print str(counter)+" airports to process."
	
	return listlist

buffylist = listbuff()
		

def singleoutput(searchstring):
	airportfound = 0
	
	#aptreader = open(inputfile, 'r')
	whichdir = searchstring[0] + "/"
	outputfile = "extracted/"+ whichdir + searchstring.replace(" ","") + ".dat"
	aptwriter = open(outputfile, 'w')
	
	#for line in aptreader.readlines():
	for line in buffy:
		if airportfound == 0:
			# regex is the snag!
			# if re.search(searchstring,line):
			if line.startswith("1  ") and searchstring == line[15]+line[16]+line[17]+line[18]:
				print "Testing line: "+line.replace("\n","")
				if line.startswith("1  "):
					print "This looks like an airport."
					airportfound = 1
					print "Processing: "+searchstring+" ... writing to file."
					aptwriter.write(line)
				else:
					print "Sorry, this is not an airport line, skipping."
					airportfound = 0
					break
					
		else:
			if line.startswith("\n") or line.startswith("\r\n"):
				airportfound = 0
				break
			aptwriter.write(line)
			
	aptwriter.close()
	del aptwriter
	print "Created '"+outputfile+"'"
	print "-------------------------------------------------"


def dothejob(chunksize):
	
	#aptlistreader = open('airports_to_process.temp', 'r')
	howmuch = 0
	
	
	print "Starting to read the list and processing airports ..."
	for listline in buffylist:
		#sleep(1)
		listline2 = listline.replace("\n","")
		string = listline2
		howmuch += 1
		#print "#"+str(howmuch)
		singleoutput(string)
		
		#del listline
		if howmuch >= chunksize:
			break

def freebuffylist(chunksize):

	howmuch = 0

	for entry in range(chunksize):		
		howmuch += 1
		buffylist.pop(0)
		if howmuch >= chunksize:
			break
	print "Removing "+str(chunksize)+" ..."
	gc.collect(2)

processed = 0

def doitinchunks(ranged):
	
	processed = chunkin
	
	for i in range(ranged):
		dothejob(chunkin)
		freebuffylist(chunkin)
		i = i + 1
	#processed = processed + chunkin
	print str(processed)+" Files processed."
		
def buffylisttemp(buffylist):
	buffywriter = open('airports_to_process.temp', 'w')
	for i in buffylist:
		buffywriter.write(i)
	buffywriter.close()
	del buffylist
	buffylist = listbuff()
		
#howmanytimes = (len(buffylist) / chunkin) + 1
howmanytimes = (maxcount / chunkin) + 1

print "With this chunksize we have to process the list "+str(howmanytimes)+" times."

howmanyinlist = len(buffylist)

for y in range(howmanytimes):
	if howmanyinlist > 0:
		doitinchunks(1)
		buffylisttemp(buffylist)
		gc.collect(2)
		y = y + 1
		
	else:
		print "FINISHED"
	

#else:
#	"No more airports left to process, looks like success."

