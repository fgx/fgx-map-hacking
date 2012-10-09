/*!
\mainpage The Fgx Map Project

\section Intro Introduction

@todo: Gral to write sppech

\section ProjectLayout Project Layout

\subsection d_config  config/
	- This contains the configuration for data, apps and projects
	
\subsection d_dev_docs dev-docs/
	- The documentation for this project is created with \ref doxygen 
	- The source for this test you are reading is in dev_docs/doc_source/pages.cpp 
	
\subsection d_fgx fgx/
	- This is the \b fgx python lib
	- Hopefully we can make this a bit more of a global lib
	- This \b fgx/ directory is documented with \ref doxygen


Check:
  - \ref www_static 
  - \ref RelatedProjects



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