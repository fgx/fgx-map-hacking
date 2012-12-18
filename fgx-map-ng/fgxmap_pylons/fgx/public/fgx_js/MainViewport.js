
Ext.define("FGx.MainViewport", {

extend:  "Ext.container.Viewport", 

	
widgets: {
	FlightsViewWidget: null,	
	NetworkStatusWidget: null,
	DbBrowser: null,
	FlightPlansWidget: null
},

//===========================================================
//== Flights data LIVE state
// This this is location of the the "multiplayer stuff"..
refresh_rate: 0,
//runner: new Ext.util.TaskRunner(),

//= this store is passed around.. its global kinda

xFlightsStore: Ext.create("Ext.data.JsonStore", {
	idProperty: 'callsign',
	storeId: "flights_store",
	fields: [ 	
		{name: 'flag', type: 'int'},
		{name: 'check', type: 'int'},
		{name: "callsign", type: 'string'},
		{name: "server", type: 'string'},
		{name: "model", type: 'string'},
		{name: "lat", type: 'float'},
		{name: "lon", type: 'float'},
		{name: "alt_ft", type: 'int'},
		{name: "spd_kts", type: 'int'},
		//{name: "alt_trend", type: 'string'},
		{name: "hdg", type: 'int'}
	],
	url: '/ajax/mpnet/flights/crossfeed',
	root: 'flights',
	remoteSort: false,
	sortInfo: {
		field: "callsign", 
		direction: 'ASC'
	},
	autoLoad: false,
}),
xMpStatusStore: Ext.create("Ext.data.JsonStore", {
	idProperty: 'no',
	storeId: "mpstatus_store",
	fields: [ 	
		{name: 'no', type: 'int'},
		{name: 'fqdn', type: 'string'},
		{name: "ip", type: 'string'},
		{name: "last_checked", type: 'string'},
		{name: "last_seen", type: 'string'},
		{name: "lag", type: 'int'},
		'country', 'time_zone', 'lat', 'lon'
	],
	url: '/ajax/mpnet/status',
	root: 'mpstatus',
	remoteSort: false,
	sortInfo: {
		field: "no", 
		direction: 'ASC'
	},
	autoLoad: false,
}),

update_flights: function(){
	this.xFlightsStore.load();
},

on_refresh_toggled: function(butt, checked){
	//console.log("on_refresh_toggled", butt.refresh_rate, butt.checked);
	
	butt.setIconClass( checked ? "icoOn" : "icoOff" );
	
	//= set new refresh var
	this.refresh_rate = butt.refresh_rate;
	
	//= stop any runners.. but this will/might callback though.. does not cancel sent request..
	this.runner.stopAll();
	
	//= start again with new rate..
	if(this.refresh_rate > 0){
		this.runner.start({
			interval: this.refresh_rate * 1000,
			run: this.update_flights, 
			scope: this		
		});
	}
},



on_flight_plans_widget: function(butt){
	if(!this.widgets.FlightPlansWidget){
		this.widgets.FlightPlansWidget = new FGx.FlightPlansWidget({
			//flightsStore: this.xFlightsStore,
			//refresh_rate: this.refresh_rate,
			title: "Flight Plans", 
			closable: true,
			xHidden: false
		});
		this.get_tab_panel().add(this.widgets.FlightPlansWidget);
	}
	//console.log(this.widgets);
	this.get_tab_panel().setActiveTab(this.widgets.FlightPlansWidget);
},


on_flights_widget: function(butt){
	if(!this.widgets.FlightsViewWidget){
		
		this.widgets.FlightsViewWidget = Ext.create("FGx.mpnet.FlightsViewWidget", {
			title: "Flights", 
			closable: true,
			xHidden: false
		});
		this.get_tab_panel().add(this.widgets.FlightsViewWidget);
		console.log("created");
	}
	this.get_tab_panel().setActiveTab(this.widgets.FlightsViewWidget);
},

on_network_status_widget: function(butt, checked){
	if(!this.widgets.NetworkStatusWidget){
		this.widgets.NetworkStatusWidget = new FGx.NetworkStatusWidget({
			title: "Network Status", 
			closable: true,
			xHidden: false
		});
		this.get_tab_panel().add(this.widgets.NetworkStatusWidget);
		
	}
	this.get_tab_panel().setActiveTab(this.widgets.NetworkStatusWidget);
},
on_db_browser_widget: function(butt, checked){
	if(!this.widgets.DbBrowser){
		this.widgets.DbBrowser = new FGx.DbBrowser({
			closable: true
		});
		this.get_tab_panel().add(this.widgets.DbBrowser);
	}
	this.get_tab_panel().setActiveTab(this.widgets.DbBrowser);
},
//=================================================================================
// Map Panels
//=================================================================================

open_map:  function(obj){
	//console.log("-----------------------------------------");
	console.log(">> MainViewort.open_map", obj.title, obj.iconCls, obj.lat, obj.lon, obj.zoom, obj.closable);
	//return;
	var newMap = Ext.create("FGx.map.MapViewWidget", {xConfig: obj, title: obj.title, iconCls: obj.iconCls});
	this.get_tab_panel().add(newMap);
	this.get_tab_panel().setActiveTab(newMap);
	console.log("adddtab");
},

on_goto: function(butt){
	this.open_map( butt.text, butt.lat, butt.lon, butt.zoom, true);
},


//=======================================
//== Tab Panel
get_tab_panel: function(){
	
	if(!this.xTabPanel){
		this.xTabPanel = Ext.create("Ext.tab.Panel", {
			region: "center",
			layout: "fit",
			tabPosition: "top",
			frame: false,  border: false, bodyBorder: false,
			activeTab: 0,
			ssheight: 500
		});
		this.xTabPanel.on("tabchange", function(foo, bar){
			//console.log("tabchanged");
		}, this);
		this.xTabPanel.on("remove", function(panel, widget){
			
			//console.log("remove", widget.fgxType);
			
			this.widgets[widget.fgxType] = 0;
			return;
			if(widget.fgxType == "FlightsViewWidget"){
				this.widgets.flightsGrid = 0;
				
			}else if(widget.fgxType == "NetworkStatusWidget"){
				this.widgets.NetworkStatusWidget = 0;
				
			}else if(widget.fgxType == "DbBrowser"){
				this.widgets.DbBrowser = 0;
				
			}else if(widget.fgxType == "FlightPlansWidget"){
				this.widgets.FlightPlansWidget = 0;
			}
		}, this);
	}
	return this.xTabPanel;
},

on_url_action: function(butt, foo){
	//console.log("on)urlaction", butt, butt.xMode);
	var xm = butt.xMode;
	if(xm == "window"){
		window.open(butt.url);
	}else{
		var newTab = new FGx.IFramePanel({
			url: butt.url, title: butt.text
		});
		this.get_tab_panel().add(newTab);
		this.get_tab_panel().setActiveTab(newTab);
	}
},


initComponent: function(){
	
	
	Ext.apply(this, {
		layout: "border",
		frame: false,
		plain: true,
		border: false,
		items: [
		
			// TabBar in Center
			this.get_tab_panel(),
		
			//= Top Toolbar = North
			{xtype: "panel",
				region: "north",
				frame: false, plain: true, border: false, hideBorders: true,
				margins: {top:0, right:0, bottom:5, left:0},
				hideHeader: true,
				tbar: [
					{xtype: 'tbspacer', width: 5},
					//"-",
					{text: "New Map", iconCls: "icoMapAdd", 				
						menu: [
							{text: "World", handler: this.on_goto, scope: this,
								zoom: 5, lat: 47.467, lon: 8.5597,
							},
							"-",
							{text: "Africa", disabled: true },
							{text: "Austrailia" , disabled: true},
							{text: "Europe" , disabled: true},
							{text: "Far East" , disabled: true},
							
							{text: "USA" , disabled: true},
							"-",
							{text: "Amsterdam", aptIdent: "EHAM", lat: 52.306, lon:4.7787, zoom: 10,
								handler: this.on_goto, scope: this},
							{text: "London", aptIdent: "EGLL",  lat: 51.484, lon: -0.1510, zoom: 10,
								handler: this.on_goto, scope: this},
							{text: "Paris", aptIdent: "LFPG", lat: 48.994, lon: 2.650, zoom: 10,
								handler: this.on_goto, scope: this},
							{text: "San Fransisco", aptIdent: "KSFO", lat: 37.621302, lon: -122.371216, zoom: 10,
								handler: this.on_goto, scope: this},
							{text: "Zurich", aptIdent: "LSZH", lat: 47.467, lon: 8.5597, zoom: 10,
								handler: this.on_goto, scope: this},
						]
					},
					"-",
					//{xtype: 'tbspacer', width: 10},
					///"-",
					{text: "Flights", iconCls: "icoFlights", 
						handler: this.on_flights_widget, scope: this
					},
					"-",
					{text: "Flight Plans", iconCls: "icoFlightPlans", xtype: "splitbutton",
						handler: this.on_flight_plans_widget, scope: this,
						menu:[
							//TODO: new FGx.UrlAction({text: "RouteFinder - rfinder.asalink.net/free/", url: //"http://rfinder.asalink.net/free/", M: this}),
						]
					},
					"-",
					{text: "Network Status", iconCls: "icoMpServers", 
						handler: this.on_network_status_widget, scope: this
					},
					"-",
					{iconCls: "icoDev", tooltip: "Developer", text: "Developer",
						menu: [
							{iconCls: "icoDatabase", text: "Database Schema", handler: this.on_db_browser_widget, scope: this}
						]
					},
					"-",
					{tooltip: "About FGx", iconCls: "icoHelp", text: "About", disabled: true,
						handler: this.on_show_iframe, scope: this,
						url: "/about_iframe"
					},
					"-",
					//{text: "Settings", iconCls: "icoSettings"},
					//"-",
					
					//== Refresh MP
					{xtype: 'tbspacer', width: 50},
					"-",
					{xtype: "tbtext", text: "MP Refresh >&nbsp;", tooltip: "MultiPlayer refresh in seconds"},
					this.get_refresh_buttons(),
					"-",
					
					"->",
					//"-",
		
					//== FlightGear Menu
					"-",
					{text: "FlightGear", iconCls: "icoFlightGear", disabled: true
					
					},
					"-",	
					
					//== FGx Menu
					{text: "FGx", iconCls: "icoFgx", 
						menu: [
							{text: "Issues", url: "http://fgx.ch/projects/fgx-map/issues",
								handler: this.on_open_url, scope: this,
							},
							{text: "Git View", url: "http://git.fgx.ch/fgx-map/",
								handler: this.on_open_url, scope: this 
							},
							{text: "Chili", url: "http://fgx.ch/projects/fgx-map/",
								handler: this.on_open_url, scope: this 
							}
										
						]
					},
					"-",
					{text: "Login", iconCls: "icoLogin", disabled: true},
					//"-",
					{xtype: 'tbspacer', width: 10}
						
				]
			}			
		]
	});
	this.callParent();
	
}, // initComponent	


initialize:  function(){
	//return;
	//= Add default main map
	this.open_map({title: "Main Map", closable:false})
	return;
	//= Start MP Refresh 
	if(this.refresh_rate > 0){
		this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
	}
},

get_refresh_buttons: function(refresh_rate){
	var items = [];
	var arr = [0, 2, 3, 4, 5, 10, 20];
	for(var i = 0; i < arr.length; i++){
		var x = arr[i];
		items.push({
			text: x == 0 ? "Off" : x < 10 ? x + "&nbsp;" : x, 
			//width: 50,
			iconCls: this.refresh_rate == x ? "icoOn" : "icoOff", 
			enableToggle: true,   
			width: this.tbw,
			pressed: this.refresh_rate == x,
			toggleGroup: "ref_rate", 
			refresh_rate: x, 
			toggleHandler: this.on_refresh_toggled,
			scope: this
		})
	}
	return items;
},

//= TODO: Tiggered for reshresh now
refresh_now: function(){
	console.log("refresh_now");
	
	this.get_flights_store().load();
},

on_open_url: function(butt){
	window.open(butt.url);
	return
	var iFrame =  new FGx.IFramePanel({
		url: butt.url, title: butt.text
	});
	this.get_tab_panel().add(iFrame);
	this.get_tab_panel().setActiveTab(iFrame);
}


}) //< FGx.MainViewport
