FGx Map

This is the app you all been waiting for ;-) hopefully...

Just presents a map, and a list of all the stuff u want..
Mas distribution is what we have later, but this is the start..

This Project is a self contained fgxmap server and intended replacment for mpmap
postgis upstream and full on
cached data downstream and simple play for region

Note: we can even frop a php folder i here, is we use ajax, memcached, or file cached..
It also send websockets.. and before u get exited, stop using IE,, lets start with webkit...



Required:
pylons, jinja2, sqlalchemy, geoalchemy


sudo easy_install Pylons
sudo easy_install SQLAlchemy
sudo easy_install GeoAlchemy
sudo easy_install pyGeoIP

--------------------------------------
maxmind
--------------------------------------
http://www.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
http://www.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz


--------------------------------------
Installation and Setup
--------------------------------------

copy the skel_dev.ini to for your local setup 

> cp skel_dev.ini local.ini

ammend the local.ini to local enviroment 
* important are
  sql_aclhemy_url
  temp_dir # if importing
  


setup the database with

> paster setup-app local.ini


Run the app

> paster serve --reload local.ini


## For production
Use the skel_prod.ini which switches off debuging and debug logginng (error logs only)

and start without reload
> paster serve local.ini


read HACKING.txt for more


