This file is for you to describe the fgxmap application. Typically
you would include information such as the information below:

Installation and Setup
======================

----------------------------------------
1) Requirements
----------------------------------------
This needs the following packages

easy_install 

Pylons Jinja2 SQLAlchemy GeoAlchemy SimpleJson



----------------------------------------
2) Local Config
----------------------------------------
> copy the 
development.ini.skel
> to
development.ini
(or gral.ini or geoff.ini)

U need to change the sqlalchemy url to you local flavour


----------------------------------------
3) setup the database
----------------------------------------
use the following command to creat
the db struct

paster setup-app ./development.ini



----------------------------------------
4) Run the webserver with
----------------------------------------

paster serve --reload ./development.ini

and then browse http://locahost:5000

Note the --reload forces the server to resart
after any local file changes (slows things down)





