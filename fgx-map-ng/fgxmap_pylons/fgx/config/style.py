
from pylons import config

from string import Template

G = config['pylons.app_globals']


##==============================================================
## local_icons are in the public path, eg /images/foo.png
local_icons = {}

local_icons['icoFgx'] = "fgx-cap-16.png"
local_icons["icoAirport"] = "apt.png"
local_icons["icoFix"] = "vfr_fix.png"
local_icons["icoNdb"] = "ndb.16.png"
local_icons["icoVor"] = "vor.png"
local_icons["icoClr"] = "go.gif"


##===========================================================================
## icons is the fam fam from http://fgx-static/icons/famfam_silk/*
icons = {}


icons['icoLogin'] = "key.png"

icons['icoRefresh'] = "refresh.gif"

icons['icoOn'] = "bullet_pink.png"
icons['icoOff'] = "bullet_black.png"


icons['icoBookMarkAdd'] = "book_add.png"

icons['icoSettings'] = "cog.png"

icons['icoCallSign'] = "page_white_c.png"


icons['icoFlights'] = "text_horizontalrule.png"

icons['icoMapCore'] = "map.png"
icons['icoMap'] = "map.png"
icons['icoMapAdd'] = "map_add.png"

icons['icoMpServers'] = "server_database.png"

icons['icoBlue'] = "bullet_blue.png"
icons['icoOrange'] = "bullet_orange.png"
icons['icoPink'] = "bullet_pink.png"
icons['icoGreen'] = "bullet_green.png"
icons['icoRed'] = "bullet_red.png"
icons['icoWhite'] = "bullet_white.png"
icons['icoYellow'] = "bullet_yellow.png"


icons["icoUsers"] = "group.png"
icons["icoUser"] = "user.png"
icons["icoUserAdd"] = "user_add.png"
icons["icoUserEdit"] = "user_edit.png"
icons["icoUserDelete"] = "user_delete.png"



icons["icoCancel"] = "bullet_black.png"
icons["icoSave"] = "accept.png"




icons["icoRefreshStop"] = "clock_stop.png"
icons["icoRefreshRun"] = "clock_run.png"


## END Icons Def <<


def get_icons_css():
	
	s = ''
	
	for k in sorted(local_icons.keys()):
		s += ".%s{background-image: url('/images/%s') !important; background-repeat: no-repeat;}\n" %  (k, local_icons[k])
	s += "\n\n" # incase
	
	for k in sorted(icons.keys()):
		s += ".%s{background-image: url('%s/icons/famfam_silk/%s') !important; background-repeat: no-repeat;}\n" %  (k, G.static_url, icons[k])
	s += "\n\n" # incase
	


	return s
	
	