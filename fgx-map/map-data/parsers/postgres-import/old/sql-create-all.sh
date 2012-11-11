#!/usr/bin/bash
#
# (c) 2012, Yves Sablonier, Zurich
# GPLv2 or later
# Do not change or remove this copyright notice.
#

date

for FILE in ../../data/xplane-single/*/*.dat
	do
	echo 'Processing '$FILE
	python sql-creator.py $FILE
done

date