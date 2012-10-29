#!/usr/bin/bash
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

date

for FILE in ../../parsers/apt-extractor/extracted/*/*.dat
	do
	echo 'Processing '$FILE
	python import_airport.py $FILE
done

date