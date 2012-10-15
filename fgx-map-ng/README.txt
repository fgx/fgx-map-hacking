FGx Map ToolKit


--------------------------------
PreAmble + dream on...
--------------------------------

This project is under active devel, so some things
may not work, be placeholders, etc. but under active devel

The current map server is working, so the goal of this 
project is to combine the efforts together

Roles
 - Its a toolkit, so the idea is u chackit out, and use different parts,
 - eg marble map and desktop required for  local playground
 - a server is aa import or configuration





-------------------------------------
Goal
-------------------------------------
- Create a complete project that 
  is used to create maps,
- Include all the tools from
  - Installers - managed compile etc
  - Web services with django
  - Map Services with Tilecached
  - Documentation
  - playground for fun
  - Desktop gui for map devel

Simple shell commands to do focused tasks
 eg
## 
install check


----------------------------------------
Platform
----------------------------------------
The platfrom was decided as they 
are active in spacial space
- PostGIS2 ie Postgres with spaciale xtentions
- Ddhango and GeoDjanjo dor playground
- GeoExt - a client side toolkit built on
  - OpenLayers
  - Ext-3.4 - the gpl.dodgy licences Ext lib which works.



Django and 
The fgx/ directory contains teh django app..

cd fgx

## create config
cp local_settings.skel.py local_settings.py
## and modify to taste

## populate db
./manage.py syncdb

## Run Server
./manage.py runserver



--------------------------------
Structure
--------------------------------

config/
  Contains the configuration for map data, etc

fgx/
  the Django wsgi app - but also shell purposed



dev-docs/
  The doxygen developer docs (work in progress)

etc/
 Placeholder fodler where config files are written to

examples/
  Example configurations, scripts etc









---------------------------------------
xplane
---------------------------------------

- This command will lists remove files from data.xplane
- Pulls a file to local

--------------------------------------

Platform:

Curr:

postgres 9.1

Need a script or a PPAa preferably



Run the app
  > ./run_gui.pyw



Make the docs with
./make_docs.sh

then read
>  dev-docs/html/index.html



apt-get reomove postgis libgeos-v.e.r


