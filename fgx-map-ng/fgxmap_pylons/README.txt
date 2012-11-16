FGx Map

This is the app you all been waiting for..

Just presents a map, and a list of all the stuff u want..
Mas distribution is what we have later, but this is the start..

This Project is a self contained fgxmap server and intended replacment for mpmap
postgis upstream and full on
cached data downstream and simple play for region

Note: we can even frop a php folder i here, is we use ajax, memcached, or file cached..
It also send websockets.. and before u get exited, stop using IE,, lets start with webkit...



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


