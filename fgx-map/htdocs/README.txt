
FGx Map Server
**************

(c) 2011 Yves Sablonier, Zürich

This is a small mapping project started once 2011 by Yves Sablonier (flightgear@sablonier.ch). 
Please do not remove any copyright notice in any of the files. 

LICENCE
-------
Code is licenced under GPLv2, graphics and data lives under CC-BY-SA-NC 3.0 
(when it is not stated otherwise). Please read the public available licence text to 
know what you can do with this code/data and what you should NOT.
http://www.gnu.org/licenses/gpl-2.0.html#SEC3
http://creativecommons.org/licenses/by-nc-sa/3.0/

DESCRIPTION
-----------
FGx Map comes for FlightGear Open Source Flightsimulator (GPLv2). 
The mapserver runs mapnik2 with WMS service, famous openlayers as frontend, 
fast tilecache, gdal/ogr2ogr and postgres/postgis. Map data comes from 
various places, i.e. from Natural Earth (public domain), USGS/NED (public domain), 
XPlane Data (GPLv2), Flightgear Data (GPLv2). 
Caution: GIS Data and graphics from Yves Sablonier on the server coming with 
this application are lincenced cc-by-sa-nc, means NO COMMERCIAL USE ! 
Some airnav data is provided with permission from Paul Tomblin (​http://www.xcski.com), 
airspace data comes from Worldwide Soaring Turnpoint Exchange (John Leibacher 
and contributors).

DISCLAIMER
----------
FGx mapservers data and maps have the same disclaimer like I found it at Soaring 
Turnpoint Exchange: All data and information contained in any of the data files 
are provided without guarantee as to their completeness or correctness. Any conclusions 
drawn from these data and information are the sole responsibility of the user. 
This information may not be accurate or current and is not valid for navigation or 
flight planning. No warranty of fitness for any purpose is made or implied. Always 
consult the official publications for current and correct information. 
This service is provided free of charge with no warrantees, expressed or implied. 

This map application makes use of a lot of different open source software 
written by hundreds of open source maintainers for years:
- Apache and nginx, fastcgi
- Tilecache
- Mapnik
- OpenLayers, Proj4
- GDAL/OGR2OGR
- Postgres/Postgis

And for the project development:
- git, gitolite, cgit, trac

etc.

HOW TO CONTRIBUTE
-----------------
Feel free to send me an email (flightgear.at.sablonier.ch). 
Every contribution is very welcome. Mapping is something for big groups of geo nerds, 
it is a lot of work ;-) I spent months in this project, on other experimental maps, 
the graphics, getting running servers. Oh, and all this code to understand ...
I am mainly a graphic designer and artist and not a coder, but it is ok this time. 
Also my children helped me here and there with drawing and topology, and now, anyway, 
mapping and providing a mapserver is REAL FUN !

THANKS
------
Big thanks goes to all people providing public GIS data and Open Source projects and code. 
My personal thanks goes to Martin Spott who runs THE mapserver at mapserver.flightgear.org. 
Without him this project will never have been started ;-) Many thanks also to Artem Pavlenko
Dane Springmeyer and other Mapnik contributors, making this renderer possible. 

Other thanks goes to Geoff McLane and Pete Morgan, as ever, who contributed to the main 
project on this server, the FGx FlightGear Launcher. And of course thanks to core 
development team of FlightGear and all the other contributers working so hard for one of 
the best open source project ever.


