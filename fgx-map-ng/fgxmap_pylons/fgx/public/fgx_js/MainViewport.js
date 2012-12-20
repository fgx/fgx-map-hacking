/*global Ext: false, console: false, FGx: false */

Ext.define("FGx.MainViewport", {

extend:  "Ext.container.Viewport", 

	
widgets: {
	FlightsViewPanel: null,	
	NetworkStatusPanel: null,
	DbBrowser: null,
	RoutesBrowser: null,
	FlightPlansWidget: null,
	
},

//===========================================================
//== Flights data LIVE state
// This this is location of the the "multiplayer stuff"..
refresh_rate: 0,
runner: Ext.create("Ext.util.TaskRunner", {}),

xFlightsStore: Ext.create("Ext.data.JsonStore", {
	model: "mFlight",
	storeId: "flights_store",
	proxy: {
		type: "ajax",
		url: '/ajax/mpnet/flights/crossfeed',
		reader :{
			type: "json",
			root: 'flights'
		}
	},
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
	Ext.getStore("flights_store").load();
},

on_refresh_toggled: function(butt, checked){
	
	butt.setIconCls( checked ? "icoOn" : "icoOff" );
	
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
	if(!this.widgets.FlightsViewPanel){
		
		this.widgets.FlightsViewPanel = Ext.create("FGx.mpnet.FlightsViewPanel", {
			title: "Flights", 
			closable: true,
			xHidden: false
		});
		this.get_tab_panel().add(this.widgets.FlightsViewPanel);
		console.log("created");
	}
	this.get_tab_panel().setActiveTab(this.widgets.FlightsViewPanel);
},

on_network_status_panel: function(butt, checked){
	if(!this.widgets.NetworkStatusPanel){
		this.widgets.NetworkStatusPanel = Ext.create("FGx.mpnet.NetworkStatusPanel", {
			title: "Network Status", 
			closable: true,
			xHidden: false
		});
		this.get_tab_panel().add(this.widgets.NetworkStatusPanel);
		
	}
	this.get_tab_panel().setActiveTab(this.widgets.NetworkStatusPanel);
},
on_db_browser_widget: function(butt, checked){
	if(!this.widgets.DbBrowser){
		this.widgets.DbBrowser = Ext.create("FGx.dev.DbBrowser", {
			closable: true
		});
		this.get_tab_panel().add(this.widgets.DbBrowser);
	}
	this.get_tab_panel().setActiveTab(this.widgets.DbBrowser);
},
on_routes_browser_widget: function(butt, checked){
	if(!this.widgets.RoutesBrowser){
		this.widgets.RoutesBrowser = Ext.create("FGx.dev.RoutesBrowser", {
			closable: true
		});
		this.get_tab_panel().add(this.widgets.RoutesBrowser);
	}
	this.get_tab_panel().setActiveTab(this.widgets.RoutesBrowser);
},


//=================================================================================
// Map Panels
//=================================================================================

open_map:  function(obj){
	//console.log(">> MainViewort.open_map", obj.title, obj.iconCls, obj.lat, obj.lon, obj.zoom, obj.closable);
	var newMap = Ext.create("FGx.map.MapViewPanel", {xConfig: obj, title: obj.title, iconCls: obj.iconCls});
	this.get_tab_panel().add(newMap);
	this.get_tab_panel().setActiveTab(newMap);
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
			if(widget.fgxType == "FlightsViewPanel"){
				this.widgets.flightsGrid = 0;
				
			}else if(widget.fgxType == "NetworkStatusPanel"){
				this.widgets.NetworkStatusPanel = 0;
				
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
						handler: this.on_network_status_panel, scope: this
					},
					"-",
					{iconCls: "icoDev", tooltip: "Developer", text: "Developer",
						menu: [
							{iconCls: "icoDatabase", text: "Database Schema", handler: this.on_db_browser_widget, scope: this},
							{iconCls: "icoDatabase", text: "URL Mapping", handler: this.on_routes_browser_widget, scope: this}
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
					{text:  "Off" , iconCls: "icoOn", enableToggle: true,   
						width: this.tbw, pressed: true,allowDepress: false,
						toggleGroup: "ref_rate",  refresh_rate: 0, 
						toggleHandler: this.on_refresh_toggled,	scope: this
					},
		   		   	{text:  "2" , iconCls: "icoOff", enableToggle: true,    
						width: this.tbw, allowDepress: false,
						toggleGroup: "ref_rate",  refresh_rate: 2, 
						toggleHandler: this.on_refresh_toggled,	scope: this
					},
		   			{text:  "3" , iconCls: "icoOff", enableToggle: true,   
						width: this.tbw, allowDepress: false,
						toggleGroup: "ref_rate",  refresh_rate: 3, 
						toggleHandler: this.on_refresh_toggled,	scope: this
					},
		   			{text:  "5" , iconCls: "icoOff", enableToggle: true,   
						width: this.tbw, allowDepress: false,
						toggleGroup: "ref_rate",  refresh_rate: 5, 
						toggleHandler: this.on_refresh_toggled,	scope: this
					},
		   			{text:  "10" , iconCls: "icoOff", enableToggle: true,   
						width: this.tbw, allowDepress: false,
						toggleGroup: "ref_rate",  refresh_rate: 10, 
						toggleHandler: this.on_refresh_toggled,	scope: this
					},
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
	//return;
	//= Start MP Refresh 
	if(this.refresh_rate > 0){
		this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
	}
},



//= TODO: Tiggered for reshresh now
refresh_now: function(){
	console.log("refresh_now");
	
	this.get_flights_store().load();
},

on_open_url: function(butt){
	window.open(butt.url);
	return
	// TODO
	var iFrame =  new FGx.IFramePanel({
		url: butt.url, title: butt.text
	});
	this.get_tab_panel().add(iFrame);
	this.get_tab_panel().setActiveTab(iFrame);
}


});  //< FGx.MainViewport
