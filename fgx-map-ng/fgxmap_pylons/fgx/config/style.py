
from pylons import config

from string import Template

G = config['pylons.app_globals']


icons = {}


icons['icoFgx'] = "fgx-cap-16.png"
icons['icoLogin'] = "http://ico.daffodil.uk.com/key.png"

icons['icoRefresh'] = "http://ico.daffodil.uk.com/refresh.gif"

icons['icoOn'] = "http://ico.daffodil.uk.com/bullet_pink.png"
icons['icoOff'] = "http://ico.daffodil.uk.com/bullet_black.png"


icons['icoBookMarkAdd'] = "http://ico.daffodil.uk.com/book_add.png"

icons['icoSettings'] = "http://ico.daffodil.uk.com/cog.png"

icons['icoCallSign'] = "http://ico.daffodil.uk.com/page_white_c.png"


icons['icoFlights'] = "http://ico.daffodil.uk.com/text_horizontalrule.png"

icons['icoMapCore'] = "http://ico.daffodil.uk.com/map.png"
icons['icoMap'] = "http://ico.daffodil.uk.com/map.png"
icons['icoMapAdd'] = "http://ico.daffodil.uk.com/map_add.png"

icons['icoMpServers'] = "http://ico.daffodil.uk.com/server_database.png"


"""
.icoCancel" = "http://ico.daffodil.uk.com/bullet_black.png"
.icoSave" = "http://ico.daffodil.uk.com/accept.png"

.icoClr" = "http://ico.daffodil.uk.com/go.gif"


.icoRefreshStop" = "http://ico.daffodil.uk.com/clock_stop.png"
.icoRefreshRun" = "http://ico.daffodil.uk.com/clock_run.png"


.icoAirport"apt.png"
.icoFix"vfr_fix.png"
.icoNdb"ndb.png"
.icoVor"vor.png"


.icoUsers" = "http://ico.daffodil.uk.com/group.png"
.icoUser" = "http://ico.daffodil.uk.com/user.png"
.icoUserAdd" = "http://ico.daffodil.uk.com/user_add.png"
.icoUserEdit" = "http://ico.daffodil.uk.com/user_edit.png"
.icoUserDelete" = "http://ico.daffodil.uk.com/user_delete.png"


.icoBlue" = "http://ico.daffodil.uk.com/bullet_blue.png"
.icoOrange" = "http://ico.daffodil.uk.com/bullet_orange.png"
.icoPink" = "http://ico.daffodil.uk.com/bullet_pink.png"
.icoGreen" = "http://ico.daffodil.uk.com/bullet_green.png"
.icoRed" = "http://ico.daffodil.uk.com/bullet_red.png"
.icoWhite" = "http://ico.daffodil.uk.com/bullet_white.png"
.icoYellow" = "http://ico.daffodil.uk.com/bullet_yellow.png"


icons['icoInvis'] = 'transparent.png';

icons['icoDashBoard'] = 'plugin.png';
icons['icoLanServer'] = 'server.png';

icons['icoLink'] = 'arrow_switch.png';

icons['icoAndroid'] = 'ipod.png';

##/* Widgets **************************************/
icons['icoAdd'] = 'add.png';
icons['icoEdit'] = 'page_white_edit.png';
icons['icoDelete'] = 'delete.png';
icons['icoMerge'] = 'shape_ungroup.png';

icons['icoHelp'] = 'help.png';
icons['icoHome'] = 'house.png';

icons['icoRefresh'] = 'arrow_refresh.png';
icons['icoRefresh2'] = '';
#icons['icoGo'] = 'arrow_rotate_clockwise.png';
icons['icoSave'] = 'accept.png';
icons['icoCancel'] = 'bullet_black.png';
icons['icoClipboard'] = 'page_paste.png';
icons['icoGo'] = 'control_play_blue.png';
icons['icoClose'] = 'cross.png';

icons['icoGroupBy'] = 'text_padding_top.png';


#icons['icoMore'] = 'bullet_arrow_down.png';
icons['icoShowMore'] = 'zoom_in.png';
icons['icoShowLess'] = 'zoom_out.png';


icons['icoMe'] = 'emoticon_tongue.png';

icons['icoEmail'] = 'email.png';
icons['icoSms'] = 'phone.png';
icons['icoTel'] = 'telephone.png';
icons['icoFax'] = 'newspaper.png';
icons['icoMessage'] = 'text_signature.png';
icons['icoFreeText'] = 'textfield.png';


##/* Widgets **************************************/
icons['icoBlack'] = 'bullet_black.png';
icons['icoBlue'] = 'bullet_blue.png';
icons['icoGreen'] = 'bullet_green.png';
icons['icoOrange'] = 'bullet_orange.png';
icons['icoPink'] = 'bullet_pink.png';
icons['icoPurlple'] = 'bullet_purple.png';
icons['icoRed'] = 'bullet_red.png';
icons['icoYellow'] = 'bullet_yellow.png';
icons['icoDetails'] =  'bullet_white.png';

icons['icoSearch'] = 'find.png';


##/* Form **************************************/
icons['icoClean'] = 'bullet_black.png';
icons['icoDirty'] = 'bullet_red.png';


##/* Wizzard **************************************/
icons['icoNext'] = 'arrow_right.png';
icons['icoPrev'] = 'arrow_left.png';
icons['icoWizard'] = 'wand.png';

icons['icoForward'] = 'arrow_right.png';
icons['icoBack'] = 'arrow_left.png';

icons['icoBrowse'] = 'browse.png';

###/* Actions **************************************/
#//icons['icoUpload'] = 'arrow_up.png';
#//icons['icoDownload'] = 'arrow_down.png';
icons['icoUpload'] = 'page_white_get.png';
icons['icoDownload'] = 'page_white_put.png';

icons['icoQuit'] = 'control_eject.png';
icons['icoLogin'] = 'connect.png';


icons['icoOver10'] = 'date_error.png';
icons['icoFilter'] = 'zoom.png';
icons['icoDate'] = 'date.png';
icons['icoCalendar'] = 'calendar.png';
icons['icoCalendarAdd'] = 'calendar_add.png';
icons['icoCalendarEdit'] = 'calendar_edit.png';
icons['icoCalendarDelete'] = 'calendar_delete.png';

icons['icoHistory'] = 'chart_bar.png';

icons['icoDocs'] = 'table_multiple.png';
icons['icoExcel'] = 'page_excel.png';
icons['icoPdf'] = 'page_white_acrobat.png';

icons['icoLogout'] = 'book_previous.png';

icons['icoPrint'] = 'printer.png';
icons['icoPrintQ'] = 'printer.png';
icons['icoPrinters'] = 'printer.png';
icons['icoPrinter'] = 'printer.png';
#/*******************************************************************************************/
#/* Application Icons  */
#/*******************************************************************************************/

#/*# Account Related */
icons['icoAccounts'] = 'book_addresses.png'
icons['icoAccountsAll'] = 'book_go.png'
icons['icoAccount'] = 'book.png'
icons['icoAccountAdd'] = 'book_add.png'
icons['icoAccountEdit'] = 'book_edit.png'
icons['icoAccountMerge'] = 'book_link.png'

#/*# Contact Related */
icons['icoContacts'] = 'group.png'
#$desktop_icons['users'] = 'group.png';

icons['icoContact'] = 'user.png'
icons['icoContactView'] = 'user.png'
icons['icoContactAdd'] = 'user_add.png'
icons['icoContactDelete'] = 'user_delete.png'
icons['icoContactEdit'] = 'user_edit.png'

icons['icoContactOnline'] = 'user_female.png'
icons['icoContactOnlinePending'] = 'user_orange.png'
icons['icoContactActive'] = 'user.png'
icons['icoContactInActive'] = 'user_gray.png'
icons['icoPermissions'] = 'bullet_key.png'




icons['icoLocations'] = 'pictures.png'
icons['icoLocation'] = 'picture.png';
icons['icoLocationAdd'] = 'picture_add.png';
icons['icoLocationEdit'] = 'picture_edit.png';
icons['icoLocationDelete'] = 'picture_delete.png';
icons['icoLocationMerge'] = 'picture_link.png';

icons['icoBranches'] = 'building.png';
icons['icoBranch'] = 'building.png';
icons['icoBranchAdd'] = 'building_add.png';
icons['icoBranchEdit'] = 'building_edit.png';
icons['icoBranchDelete'] = 'building_delete.png';
icons['icoBranchHq'] = 'buildinghq.png';

##/* Job */
icons['icoJob'] = 'geo_job.png';
icons['icoInsitu'] = 'geo_quote.png'; ## I know reveresd
icons['icoQuote'] = 'geo_insitu.png';## I know reveresd 
icons['icoJobs'] = 'page_copy.png';
icons['icoJobAll'] = 'geo_default.png';
icons['icoJobDetails'] = 'page_white_h.png';
#$desktop_icons['jobs'] = 'page_copy.png';


icons['icoFiles'] = 'page_white_copy.png';
icons['icoFile'] = 'geo_job.png';
icons['icoFileOpen'] = 'page_white_go.png';
icons['icoFileCopy'] = 'page_white_copy.png';
icons['icoFileRename'] = 'page_white_edit.png';
icons['icoFileDelete'] = 'page_white_delete.png';

#/* Batches  */
#/*
icons['icoBatches'] = 'cart.png';

icons['icoBatchAdd'] = 'basket_add.png';
icons['icoBatchView'] = 'basket.png';
icons['icoBatchEdit'] = 'basket_edit.png';
icons['icoBatchDelete'] = 'basket_delete.png';
#*/

icons['icoBatches'] = 'cart.png';
icons['icoBatch'] = 'cart.png';
icons['icoBatchAdd'] = 'cart_add.png';
icons['icoBatchView'] = 'cart.png';
icons['icoBatchEdit'] = 'cart_edit.png';
icons['icoBatchDelete'] = 'cart_delete.png';


#/* Rates */
icons['icoRates'] = 'application_osx.png';

#/* Job Item */
icons['icoJobItem'] = 'page.png';

icons['icoJobItemAdd'] = 'page_add.png';
icons['icoJobItemEdit'] = 'page_edit.png';
icons['icoJobItemDelete'] = 'page_delete.png';


############# COC ####################
icons['icoCocs'] = 'page_white_c.png';
icons['icoCocAdd'] = 'xhtml_add.png';
icons['icoCocEdit'] = 'xhtml_valid.png';
icons['icoCocDelete'] = 'xhtml_delete.png';

#icons['icoCocs'] = 'cart.png';
#icons['icoCocAdd'] = 'cart_add.png';
#icons['icoCocEdit'] = 'cart_add.png';
#icons['icoCocDelete'] = 'cart_delete.png';

#/* Samples */
#/* icons['icoSamples'] = 'package_green.png';
#icons['icoSample'] = 'package.png';
#icons['icoSampleAdd'] = 'package_add.png';
#icons['icoSampleDelete'] = 'package_delete.png';
#*/
icons['icoSamples'] = 'tag_blue.png';
icons['icoSample'] = 'tag_green.png';
icons['icoSampleAdd'] = 'tag_blue_add.png';
icons['icoSampleDelete'] = 'tag_blue_delete.png';

icons['icoTestPoints'] = 'photos.png';
icons['icoTestPoint'] = 'photo.png';
icons['icoTestPointAdd'] = 'photo_add.png';
icons['icoTestPointEdit'] = 'photo.png';
icons['icoTestPointDelete'] = 'photo_delete.png';


###/* Stores */
icons['icoStores'] = 'bricks.png';
#//icons['icoSample'] = 'package.png';

##/* Test */
icons['icoTest'] = 'chart_line.png';
icons['icoTestAdd'] = 'chart_line_add.png';
icons['icoTestEdit'] = 'chart_line_edit.png';
icons['icoTestDelete'] = 'chart_line_delete.png';
icons['icoReport'] = 'chart_curve.png';

##/* Toolbar studd */
icons['icoStatus'] = 'page_white_database.png';
icons['icoQuickLinks'] = 'sitemap.png';

icons['icoJobItems'] = 'page_copy.png';


#/* Schedule */
icons['icoSchedule'] = 'table.png';
icons['icoScheduleAmmend'] = 'table_edit.png';
icons['icoScheduleItem'] = 'timeline_marker.png';



#//icons['icoSchedulePending'] = 'flag_blue.png';
#//icons['icoScheduleInProgress'] = 'flag_yellow.png';
#//icons['icoScheduleCompleted'] = 'flag_green.png';
icons['icoScheduleNotInProgress'] = 'bullet_red.png';
icons['icoScheduleInProgress'] = 'bullet_orange.png';
icons['icoScheduleCompleted'] = 'bullet_green.png';
icons['icoScheduleFlag'] = 'flag_red.png';

icons['icoLabsOutlook'] = 'timeline_marker.png';


icons['icoAuthLog'] = 'key.png';
icons['icoAuthLogOk'] = 'key_go.png';
icons['icoAuthLogFail'] = 'key_delete.png';
#icons['icoSysLog'] = 'script.png';

icons['icoSysLog'] = 'script.png';

icons['icoWww'] = 'world.png';
icons['icoWwwLink'] = 'world_link.png';
icons['icoWwwBrowse'] = 'world_go.png';
icons['icoWwwStats'] = 'chart_bar.png';

icons['icoWeekView'] = 'calendar_view_week.png';


icons['icoOn'] = 'bullet_green.png';
icons['icoOff'] = 'bullet_black.png';

icons['icoFilterOn'] = 'bullet_pink.png';
icons['icoFilterOff'] = 'bullet_purple.png';

icons['icoStart'] = 'control_play_blue.png';
icons['icoEnd'] = 'control_stop_blue.png';

icons['icoError'] = 'exclamation.png';
icons['icoMap'] = 'map.png';
icons['icoMapRoute'] = 'map_go.png';

icons['icoDiggs'] = 'database_table.png';
icons['icoSettings'] = 'plugin.png';


#//***********************************************************************
#//** Lab Locaions & dept
#//***********************************************************************
#/* Lab Locations */
#//$desktop_icons['lab-locations'] = 'images.png';
icons['icoLabs'] = 'shape_ungroup.png';

icons['icoLabLocations'] = 'images.png';
icons['icoLabLocationParent'] = 'folder_table.png';

icons['icoLabLocationLostFound'] = 'sum.png';




#//icons['icoLabLocation'] = 'image.png';
icons['icoLabLocationFolder'] = 'folder.png';
icons['icoLabLocationAisle'] = 'shape_align_left.png';
icons['icoLabLocationBin'] = 'shape_square.png';

icons['icoLabLocationLab'] = 'shape_ungroup.png';
icons['icoLabLocationEquip'] = 'compress.png';
icons['icoLabLocationInsitu'] = 'car.png';
icons['icoLabLocationVehicle'] = 'lorry.png';
icons['icoLabLocationRig'] = 'wrench_orange.png';
icons['icoLabLocationSkip'] = 'bin_closed.png';



icons['icoLabLocationAdd'] = 'image_add.png';
icons['icoLabLocationEdit'] = 'image_edit.png';
icons['icoLabLocationDelete'] = 'image_delete.png';






icons['icoShortcuts'] = 'arrow_inout.png';
icons['icoDev'] = 'wand.png';


icons['icoSysAdmin'] = 'style_add.png';
icons['icoGeoAdmin'] = 'style.png';

icons['icoMerge'] = 'table_relationship.png';

icons['icoFolder'] = 'folder.png'
icons['icoFolderAdd'] = 'folder_add.png'



icons['icoRootTree'] = 'sitemap_color.png'
icons['icoUsers'] = 'group_gear.png'

icons['icoBackDoor'] = 'lock_go.png'


icons['icoWebQueries'] = 'creditcards.png'
icons['icoWebQuery'] = 'css.png'
"""
def get_icons_css():
	
	s = ''
	for k in sorted(icons.keys()):
		s += ".%s{background-image: url('%s/%s') !important; background-repeat: no-repeat;}\n" %  (k, G.static_url, icons[k])
	s += "\n\n" # incase

	return s
	
	