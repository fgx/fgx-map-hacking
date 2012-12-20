##@package fgx.config.style
# @brief Css, icons, svg and other style definitions and helpers
#

from pylons import config

from string import Template

## local_icons are in this projects <b>public/</b> path, eg /images/foo.png
local_icons = {}

local_icons['icoFgx'] = "fgx-cap-16.png"
local_icons['icoFlightGear'] = "flightgear_icon.png"

local_icons["icoAirport"] = "apt.png"
local_icons["icoFix"] = "vfr_fix.png"
local_icons["icoNdb"] = "ndb.16.png"
local_icons["icoVor"] = "vor.png"
local_icons["icoClr"] = "go.gif"


## static_icons are the fam fam icon set at http://static.fgx.ch/icons/famfam_silk/
static_icons = {}

static_icons["icoAirways"] = "chart_line.png"
static_icons["icoFlightPlans"] = "page_white_actionscript.png"

static_icons['icoHelp'] = "help.png"
static_icons['icoExecute'] = "accept.png"
static_icons['icoHtml'] = "html.png"

static_icons['icoDev'] = "shape_align_bottom.png"
static_icons['icoDatabase'] = "database.png"

static_icons['icoSelectStyle'] = "color_swatch.png"

static_icons['icoLogin'] = "key.png"

static_icons['icoRefresh'] = "refresh.gif"

static_icons['icoOn'] = "bullet_pink.png"
static_icons['icoOff'] = "bullet_black.png"


static_icons['icoBookMarkAdd'] = "book_add.png"

static_icons['icoSettings'] = "cog.png"

static_icons['icoCallSign'] = "page_white_c.png"


static_icons['icoFlights'] = "text_horizontalrule.png"

static_icons['icoMapCore'] = "map.png"
static_icons['icoMap'] = "map.png"
static_icons['icoMapAdd'] = "map_add.png"
static_icons['icoMapGo'] = "map_go.png"

static_icons['icoMpServers'] = "server_database.png"

static_icons['icoBlue'] = "bullet_blue.png"
static_icons['icoOrange'] = "bullet_orange.png"
static_icons['icoPink'] = "bullet_pink.png"
static_icons['icoGreen'] = "bullet_green.png"
static_icons['icoRed'] = "bullet_red.png"
static_icons['icoWhite'] = "bullet_white.png"
static_icons['icoYellow'] = "bullet_yellow.png"


static_icons["icoUsers"] = "group.png"
static_icons["icoUser"] = "user.png"
static_icons["icoUserAdd"] = "user_add.png"
static_icons["icoUserEdit"] = "user_edit.png"
static_icons["icoUserDelete"] = "user_delete.png"



static_icons["icoCancel"] = "bullet_black.png"
static_icons["icoSave"] = "accept.png"




static_icons["icoRefreshStop"] = "clock_stop.png"
static_icons["icoRefreshRun"] = "clock_run.png"


## @brief Generate the ext css icon style
#
# The function serielises the style.local_icons and style.static_icons to css classes
# \code 
# .icoFoo{background-image: url('/images/my_foo.png') !important; background-repeat: no-repeat;}
# \endcode
# @see controllers.html_pages.HtmlPagesController.dynamic_icons_css()
# @retval str with the css
def get_icons_css():
	
	G = config['pylons.app_globals']
	
	s = ''
	
	for k in sorted(local_icons.keys()):
		s += ".%s{background-image: url('/images/%s') !important; background-repeat: no-repeat;}\n" %  (k, local_icons[k])
	s += "\n\n" # incase
	
	for k in sorted(static_icons.keys()):
		s += ".%s{background-image: url('%s/icons/famfam_silk/%s') !important; background-repeat: no-repeat;}\n" %  (k, G.static_url, static_icons[k])
	s += "\n\n" # incase
	
	return s
	
	