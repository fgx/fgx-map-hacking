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


read HACKING.txt for more


