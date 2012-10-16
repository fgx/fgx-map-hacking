FGx Map ToolKit

The idea is to create a scripted enviroment to install, create, configure and
play with the map enviroment, both on a server, and a local dev pc.

The current idea and vision is to kinda run the following sequence: run ./ 
  1 - install - toDO install all the setup and stuff u need, eg APT-get, py, py custom compile postgis2 etc
  2 - write-config - to create the db config etc local, whether on server or dev station
  3 - The Make DB steps - Buig TODO, but currently in django land and models also
  4 - xplane-download - to pull latest data from remote server - working on fix's
  5 - db-import - to import above data into the database workz only on Fix atmo
  6 - run-www - toDO launch django webserver
  7 - run-bot - Runs a simple bot and kinda working, writes to memcached atmo

--------------------------------
#1 - Install
----------------------------------
./install.py - TODO state, but packages required are in config/install.yaml
             - PLESE update the required packaged there, and version
required<
apt-get, 
postgres




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




