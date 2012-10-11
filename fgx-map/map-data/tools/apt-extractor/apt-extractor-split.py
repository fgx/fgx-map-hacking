#!/usr/bin/python
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not remove this copyright notice.
#
# This is a helper to split huge apt.dat files into chunks
# Arguments are <apt.dat> <chunksize>



import sys, csv, os
sys.path.append("/usr/local/lib/python/site-packages");

if sys.argv[1] == "--help" or sys.argv[1] == "-h" or sys.argv[1] == "":
	print "Usage: python apt-extractor-split.py <apt.dat> <splitsize>"
	print "The split size is in airports per file, i.e. 1000"
	sys.exit(0)
   
if not os.path.exists(sys.argv[1]):
	print "Sorry, file not here, and also not there. Check paths."
	print "Usage: python apt-extractor-split.py <apt.dat> <splitsize>"
	print "The split size is in airports per file, i.e. 1000"
	sys.exit(0)
	
inputfile = sys.argv[1] # apt.dat file
chunkin = int(sys.argv[2]) # how many airports

def aptbuff(aptfilename):
	allinalist = []
	linecounter = 0
	print "Starting to read the .dat file into buffy ..."
	aptreader = open(aptfilename, 'r')
	for line in aptreader.readlines():
		linecounter += 1
		allinalist += [line]
	print "Reading "+str(linecounter)+" lines"
	
	return allinalist
	
buffy = aptbuff(inputfile)

def aptcount(aptfilename):
	aptcounter = 0
	print "Counting airports ..."
	aptreader = open(aptfilename, 'r')
	for line in aptreader.readlines():
		if line.startswith('1  '):
			aptcounter += 1
	print str(aptcounter)+" airports."
	
	return aptcounter

aptcounter = aptcount(inputfile)

dir = "temp"

if not os.path.exists(dir):
	os.makedirs(dir)
else:
	print "Directory 'temp' already exist. Files will be overwritten."


howmanyfiles = (aptcounter / chunkin) +1
print "Will give "+str(howmanyfiles)+" splitted apt.dat files to process."

start = 0
stop = chunkin

for i in range(howmanyfiles):

	aptcounter = 0
	
	path = dir+"/"+"apt-split-"+str(i)+".temp"
	
	print "Processing airports "+str(start+1)+" to "+str(stop)+" into "+path
	tempwriter = open(path, 'w')

	for line in buffy:
		if line.startswith('1  '):
			aptcounter += 1
		if aptcounter > start and aptcounter < stop:
			tempwriter.write(line)

	start = start + chunkin
	stop = stop + chunkin
	
	tempwriter.close()
			

		
		


