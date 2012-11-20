
Ext.namespace("FGx");

Ext.namespace("FGx");

FGx.MainViewport = Ext.extend(Ext.Viewport, {

	
//===========================================================
//== Flights data LIVE state
// This this is location of the the "multiplyer stuff"..
// The "Flights" are stored in an object and is passed around..
/* flights: {
	refresh_rate: 0,
	runner: new Ext.util.TaskRunner(),
	store: this.get_flights_store()						  
}, NOT */


refresh_rate: 0,
runner: new Ext.util.TaskRunner(),

//= this store is passed around.. its global kinda
get_flights_store: function(){
	if(!this.xFlightsStore){
		this.xFlightsStore = new Ext.data.JsonStore({
			idProperty: 'callsign',
			fields: [ 	{name: 'flag', type: 'int'},
						{name: 'check', type: 'int'},
						{name: "callsign", type: 'string'},
						{name: "server", type: 'string'},
						{name: "model", type: 'string'},
						{name: "lat", type: 'float'},
						{name: "lon", type: 'float'},
						{name: "alt_ft", type: 'int'},
						{name: "spd_kts", type: 'int'},
						//{name: "alt_trend", type: 'string'},
						{name: "heading", type: 'string'}
			],
			url: '/ajax/mp/flights/crossfeed',
			root: 'flights',
			remoteSort: false,
			sortInfo: {
				field: "callsign", 
				direction: 'ASC'
			},
			autoLoad: false,
		});
	}
	return this.xFlightsStore;
},

update_flights: function(){
	this.get_flights_store().load();
},

on_refresh_toggled: function(butt){
	//console.log("on_refresh_toggled", butt.refresh_rate);
	
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







flightsGrid: 0,



on_flights_widget: function(butt, checked){
	console.log("on_flights_grid");
	this.flightsGrid = new FGx.FlightsGrid({
		flightsStore: this.get_flights_store(),
		refresh_rate: this.refresh_rate,
		title: "Flights", 
		closable: true,
		xHidden: false
	});
	this.get_tab_panel().add(this.flightsGrid);
	this.get_tab_panel().setActiveTab(this.flightsGrid);
},



//=================================================================================
// Map Panels
//=================================================================================

on_open_map:  function(title, lat, lon, zoom, closable){
	console.log("on_open_map", title, lat, lon, zoom, closable);
	var newMap = new FGx.MapPanel({
		title: title, closable: closable, 
		flightsStore: self.flightsStore,
		lat: lat, lon: lon, zoom: zoom
	});
	this.get_tab_panel().add(newMap);
	this.get_tab_panel().setActiveTab(newMap);
	
},

on_goto: function(butt){
	//var lonLat = new OpenLayers.LonLat(
	//		).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	//this.fireEvent("OPEN_MAP", butt.text, true, lonLat, butt.zoom);
	this.on_open_map( butt.text, butt.lat, butt.lon, butt.zoom, true);
	console.log("on_goto");
},


//=======================================
//== Tab Panel
get_tab_panel: function(){
	
	if(!this.xTabPanel){
		this.xTabPanel = new Ext.TabPanel({
			region: "center",
			tabPosition: "top",
			frame: false, plain: true, border: false, bodyBorder: false,
			activeItem: 0
		});
		this.xTabPanel.on("tabchange", function(foo, bar){
			
		}, this);
	}
	return this.xTabPanel;
},




//=======================================
//== Contructor
constructor: function(config) {
	
	config = Ext.apply({
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
					"-",
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
					{xtype: 'tbspacer', width: 10},
					"-",
					{text: "Flights", iconCls: "icoFlights", id: this.getId() + "butt-flights", 
							enableToggle: true, pressed: false, 
							handler: this.on_flights_widget, scope: this
					},
					
					"-",
					{text: "Network Status", iconCls: "icoMpServers", 
						enableToggle: true, pressed: false, id: this.getId() + "butt-server-status",
						handler: this.on_server_status, scope: this
					},
					"-",
					//{text: "Settings", iconCls: "icoSettings"},
					//"-",
					{xtype: 'tbspacer', width: 50},
					"-",
					
					{text: "Now", iconCls: "icoRefresh",  handler: this.on_refresh_now, scope: this},
					this.get_refresh_buttons(),
						
					"->",	
					"-",	
					{text: "Login", iconCls: "icoLogin", disabled: true},
					"-",
					{text: "FGx", iconCls: "icoFgx", 
						menu: [
							{text: "Issues", xUrl: "http://fgx.ch/projects/fgx-map/issues",
								handler: this.on_open_url, scope: this,
							},
							{text: "Git Source Code" ,
								menu: [
									{text: "cgit- recommended", xUrl: "http://git.fgx.ch/fgx-map/",
										handler: this.on_open_url, scope: this },
									{text: "Chili", xUrl: "http://fgx.ch/projects/fgx-map/",
										handler: this.on_open_url, scope: this }
								]
							},
							{text: "Database Browser", xUrl: "/database",
								handler: this.on_open_url, scope: this},
						
							
							
						]
					},
					{xtype: 'tbspacer', width: 10}
						
				]
			}			
		]
	}, config);
	
	FGx.MainViewport.superclass.constructor.call(this, config);
}, // Constructor	



initialize:  function(){
	//self.map.setBaseLayer( BASE_LAYERS.osm_light );
//	: new OpenLayers.LonLat(939262.20344,5938898.34882),
	this.on_open_map("Main Map", null, null, null, false)
	
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
			text: x == 0 ? "None" : x, 
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

//= Riggered for reshresh now
refresh_now: function(){
	console.log("refresh_now");
	
	this.get_flights_store().load();
},

on_open_url: function(butt){
	window.open(butt.xUrl);
}


}) //< FGx.MainViewport
