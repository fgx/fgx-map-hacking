FGx Map


Required python

sudo easy_install Pylons
sudo easy_install SQLAlchemy
sudo easy_install GeoAlchemy
sudo easy_install shapley


--------------------------------------
Installation and Setup
--------------------------------------

copy the example.ini.skel to for your local setup 

> cp example.ini.skel mysetup.ini

ammend the mysetup.ini to local enviroment. 
important are:

- temp_dir = the local temporary directory for unpacking etc (eg /tmp/fgxmap)
- sql_aclhemy_url's, 
  There are three URL for the databases for navdata, users and mpnet
  (But all these could point to the same db)

setup the database(s) with

> paster setup-app mysetup.ini


read HACKING.txt for more (TODO)


