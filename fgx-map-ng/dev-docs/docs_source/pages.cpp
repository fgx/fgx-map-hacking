/*!
\mainpage The Fgx Map Project

\section Intro Intro

Whats in the BOX ?

Well this is a complete mashup project, and it compises a set of tool to create or play with
map development. its a set  of tools, server apps, server, configs, data definitions, import tools,
compile kit, projection object, data and other stuff including an attempt at a mapual
- a set of tools to setup a ma



@todo: Gral to write sppech

\section index Docs Quick Index
 - \ref ProjectLayout
 - \ref Configuration
 - \ref run_config 
 - \ref RelatedProjects

 - Server Services
   - \ref PostGis 
   - \ref Mapnick
   - \ref TileCache
   - \ref Django
   - \ref MpBot
   
  - Browser Libs
   - \ref OSM 
   - \ref GeoExt
   - \ref Ext
   
 - Desktop Tools
  - 
  - qgis, me included pyqt app
  
   
   
 
 
 

\page ProjectLayout Project Layout

The project contains the following directories

\section d_config  config/
	- This contains the configuration for data, apps and projects
	- See the \ref Configuration page for more info

\section d_etc  etc/
	- This is a placeholder directory when configs are written to
	- Files are nromally synlinked from here eg
	  \code 
	  ln -s ./etc/config.js ./www_static/js/config.js
	  \endcode
	- See the \ref Configuration page for more info
	
	
\section d_dev_docs dev-docs/
	- The documentation for this project is created with \ref doxygen 
	- The source for this test you are reading is in \b /dev_docs/doc_source/pages.cpp 
	
\section d_fgx fgx/
	- This is the python lib, the api is at \ref namespaces
	- Hopefully we can make this a bit more of a global lib
	- This \b fgx/ directory is documented with \ref doxygen


Check:
  - \ref www_static 
  - \ref RelatedProjects


*****************************************************
\page Postgres  Postgres Db

required: 9.1 ?

install with postgres, 
and if on desktop u need the pgadmin
and if online u need psycop the python connector ruby =
\code
sudo apt-get install postgres

\endcode
 

*****************************************************
\page Configuration  Configuration
 - The general idea is to define the config in a set of files, and then use these
   to create the various client and server side files.
 - The configuration is contained in <b>.yaml</b> encoded files in the \b config/ directory.
 @see \ref run_config
 
\section config_files Config Files

\subsection resolutions_yaml resolutions.yaml
This contains a list of resoltions. This is spooled to confg.js and tilecache config
\include config/resolutions.yaml

\subsection layers_yaml layers.yaml
This contains a list of layers
\include config/layers.yaml


 
*****************************************************
\page run_config run_config.py
 - The \b run_config.py command is used to create the various configurations
 
\section run_config_options  Options
 - <b>-j</b> - Writes out javascript to <b>/etc/config.js</b>
 - <b>-t</b> - Writes out tilecache to <b>/etc/tilecache.cfg</b>
 



*****************************************************
\page RelatedProjects Releated Projects and Libraries

@note
 A lot of these libraries are server from the \b cdn.fgx.ch

\section Proj4js 
Proj4js is a JavaScript library to transform point coordinates 
from one coordinate system to another, including datum transformations.

- \b website http://trac.osgeo.org/proj4js/

\section doxygen Doxygen
	- http://doxygen.org



*****************************************************
\page cdn cdn.fgx.ch
 The Serving of javascript libraries, icons, images are from this server.
 - The sources are in git.fgx.ch:fgx.cdn
 - This is served via nginx as static. CACHE ENABLED http://cdn.fgx.ch
 - Any common libs to be unpacked in releavant type
 - All packages to be versioned by directory eg openstreemap-1.3/* as cached



*****************************************************
\page www_static Static Map

The Static Map is standalone and requires no installed software locally. All
scripts, libraries, maps etc are served from the internet, bar the script required.

\section libLoadedX Libs Loaded
 - Libs loaded from \ref cdn
 - Relies on \ref Proj4js



*/