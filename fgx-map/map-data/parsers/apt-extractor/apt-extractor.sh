#/usr/bin/bash

# Splitting apt.dat into chunks by 1000 airports
python apt-extractor-split.py ../../data/xplane-data/apt.dat 1000

# Processing splitted data files

for FILE in temp/*
	do
	echo $FILE
	python apt-extractor-chunks.py $FILE
done
