#!/bin/bash

# remve existing libs

postgis-nuke
apt-get remove libgeos

TMP="_tmp/compiles/"

## Install compile
wget geos

wget proj4

wget gdal

wget postgis2

install postgis template



