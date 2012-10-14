FGx Map Project


--------------------------------
PreAmble
--------------------------------

This project is under active devel, so some things
may not work, be placeholders, etc. but under active devel

The current map server is working, so the goal of this 
project is to combine the efforts together

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

Simple shell commands 
eg

./install.py 


./xplane-download.py 

./import.py  xplane fix

and other dreams to come true



----------------------------------------
Platform
----------------------------------------
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


