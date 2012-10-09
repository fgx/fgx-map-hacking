# -*- coding: utf-8 -*-
"""
@author: Peter Morgan
"""



from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
#import app_globals as G



class BrowserWidget( QtGui.QWidget ):

    def __init__( self, parent, page=None, compact=False, enable_api=True ):
        QtGui.QWidget.__init__( self, parent )
        """Implements An internal QtWebKit based browser"""


        self.init_loaded = False

        mainLayout = QtGui.QVBoxLayout()
        mainLayout.setContentsMargins( 0, 0, 0, 0 )
        mainLayout.setSpacing( 0 )
        self.setLayout( mainLayout )


        ##===--------------------------------------------
        ## Toolbar
        toolbar = QtGui.QToolBar()
        mainLayout.addWidget( toolbar, 0 )

        act = toolbar.addAction(  "< Back", self.on_back )
        act.setToolTip( "Back" )
        act = toolbar.addAction( "Forward >", self.on_forward )
        act.setToolTip( "Forward" )
        act = toolbar.addAction( "Refresh", self.on_refresh )
        act.setToolTip( "Refresh" )

        ##===--------------------------------------------
        ## Url Text
        self.txtUrl = QtGui.QLineEdit(  )
        if page:
            self.txtUrl.setText(page)
        toolbar.addWidget( self.txtUrl )

      



        self.browser = QtWebKit.QWebView( self )
        mainLayout.addWidget( self.browser, 2000 )
        self.connect( self.browser, QtCore.SIGNAL( "statusBarMessage(const QString&)" ), self.on_browser_status_message )
        self.connect( self.browser, QtCore.SIGNAL( "urlChanged(const QUrl&)" ), self.on_browser_url_changed )


        self.connect( self.browser, QtCore.SIGNAL( "loadStarted()" ), self.on_browser_load_started )
        self.connect( self.browser, QtCore.SIGNAL( "loadProgress(int)" ), self.on_browser_load_progress )
        self.connect( self.browser, QtCore.SIGNAL( "loadFinished(bool)" ), self.on_browser_load_finished )
        #self.connect(self.reply, QtCore.SIGNAL( 'finished()'), self.on_server_read_finished)

        #self.browser.settings().setLocalStoragePath( offline_path )
        #self.cookieJar = QtNetwork.QNetworkCookieJar()
        #self.browser.page().networkAccessManager().setCookieJar( self.cookieJar )


        self.statusBar = QtGui.QStatusBar()
        mainLayout.addWidget( self.statusBar, 0 )

        self.progress = QtGui.QProgressBar()
        self.statusBar.addPermanentWidget( self.progress )
        self.progress.setVisible( False )

        self.browser.load( QtCore.QUrl(page) )


    def init_load( self ):
        if self.init_loaded:
            return
        url_str = self.cmbLocations.itemData( self.cmbLocations.currentIndex() ).toString()
        #print "init_load = url_str", url_str
        self.send_request( url_str )
        self.init_loaded = True


    def send_request( self, url_str ):

        url = QtCore.QUrl( url_str )

        self.request = QtNetwork.QNetworkRequest()
        self.request.setUrl( url )

        G.settings.settings.beginGroup( "cookies" )
        cookies_list = []
        for ki in G.settings.settings.childKeys():
            v = str( G.settings.settings.value( "%s" % ki ).toString() )
            cookies_list.append( "%s=%s" % ( ki, v ) )
        G.settings.settings.endGroup()

        cook_string = "; ".join( cookies_list )
        self.request.setRawHeader( "Cookie", QtCore.QVariant( cook_string ).toByteArray() )

        self.browser.load( self.request )



    def on_location_combo( self, idx ):
        #print "on_location_combo", idx, self.cmbLocations.itemData( idx ).toString()
        url = QtCore.QUrl( self.cmbLocations.itemData( idx ).toString() )
        self.browser.load( url )

    def on_refresh( self ):
        self.browser.reload()

    def on_back( self ):
        self.browser.back()

    def on_forward( self ):
        self.browser.forward()


    def dddload( self, str_url=None ):
        if str_url == None:
            return

        str_url = G.settings.ini.site['www_url']
        url = QtCore.QUrl( str_url )
        self.browser.load( url )



    #################################################
    ## Browser Events
    def on_browser_status_message( self, string ):
        #print "status=", string # does nothing ????
        self.statusBar.showMessage( string )

    def on_browser_url_changed( self, url ):
        return # doesnt trigger ???
        #print "url=", url, url.toString()
        self.txtUrl.setText( url.toString() )

    def on_browser_link_clicked( self, url ):
        #print "url=", url, url.toString() # doesnt trigger ???
        self.txtUrl.setText( url.toString() )


    def on_browser_load_started( self ):
        self.progress.setVisible( True )

    def on_browser_load_progress( self, v ):
        self.progress.setValue( v )

    def on_browser_load_finished( self, foo ):
        #print "Finished"
        self.progress.setVisible( False )
        return
        cookies = self.browser.page().networkAccessManager().cookieJar().allCookies()
        #print "-------- REC COOKIES----------------_"
        G.settings.settings.beginGroup( "cookies" )
        for cookie in cookies:
            G.settings.setValue( "%s" % str( cookie.name() ), str( cookie.value() ) )
            #print "SAVE", cookie.name(), cookie.value()
        G.settings.settings.endGroup()
        G.settings.settings.sync()
