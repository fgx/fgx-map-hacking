FGx Map

Required:
pylons, jinja2, sqlalchemy, geoalchemy

--------------------------=========
Installation and Setup
--------------------------=========

copy the development.ini to for your setup

> cp development.ini mysetup.ini

ammend the .ini to local requirements

setup the database with

> paster setup-app mysetup.ini


Run the app

> paster server --reload mysetup.ini


## For production
Use the production.ini which switches off debuging and debug logginng (error logs only)

and start without reload
> paster server myprod.ini


## Note: 
Please use tabs for spacing if possible

=================================================
## Hacking
=================================================

--------------------------
Static Files
--------------------------
The public/ directory contains all the static stuff eg favicon, js/, css, images, etc
Anything in here is read first, and if there, is send to browser
(in production this is statically mapped with nginx, apache probably not)


--------------------------
routing.py
--------------------------
Then in config/routing.py, are the path mapping for the url to the 
eg the following two example, first for ajax, second for html
map.connect('/map', controller="html_pages", action="map")
map.connect('/ajax/mp/flights', controller="ajax_mp", action="flights")
map.connect('/ajax/fix/{fix}', controller="ajax_nav", action="fix")


--------------------------
controller
--------------------------
The "controller" is in the class/file in the "controllers/" directory 
eg
controllers/html_pages.py
controllers/ajax_mp.py


The controller are named after the fileName Hungarian style 
eg
class HtmlPagesController()
class AjaxMpController()
class AjaxNavController()

to create a new controller run
> paster controller my_controller 

--------------------------
action
--------------------------
The "action" is the function of the class
eg
## renders a jinja2 template from the tempaltes/ directory
def index(self):
	return render("map-ext.html") 

## returns the dict of data as json using the decorator
@jsonify
def flights(self):
	payload = dict(success=True, 
					flights=mylib.get_flights_function() )
	return payload 


## returns the fix info
@jsonify
def fix(self, fix=None):
	payload = dict(success=True, 
					flights=mylib.get_flights_function() )
	return payload 


--------------------------
Database
--------------------------

The database models are contained in
models/__init__.py
Yes, a lot of models in one file, but this makes it easier.
This is where native sqlalchemy, geoalchemy object exist.

The http://www.geoalchemy.org/ is also included for geometry types



