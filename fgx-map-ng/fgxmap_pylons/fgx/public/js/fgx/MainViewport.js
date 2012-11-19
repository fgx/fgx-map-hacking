
Ext.namespace("FGx");

Ext.namespace("FGx");

FGx.MainViewport = Ext.extend(Ext.Viewport, {

	
//===========================================================
//== FlightsStore

refresh_rate: 0,
runner: new Ext.util.TaskRunner(),

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
	this.get_flights_store.load();
},


flightsGrid: 0,

load_flights_grid: function(){
	this.flightsGrid = new FGx.FlightsGrid({
		flightsStore: this.flightsStore,
		refresh_rate: this.refresh_rate,
		title: "Flights", 
		closable: true,
		xHidden: false
	});
	
},



//=================================================================================
// Map Panels
//=================================================================================

on_open_map:  function(title, lat, lon, zoom, closable){
	var newMap = new FGx.MapPanel({
		title: title, closable: true, 
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
	this.on_open_map( butt.text, true, butt.lon, butt.lat, butt.zoom);
},



//this.mapPanels = {};
/*
ssadd_map: function(title, lat lon, zoom, closable){
	var mapPanel = new FGx.MapPanel({
		title: title, closable: closable, flightsStore: self.flightsStore,
		lonLat: lonLat, zoom: zoom
	});	
	mapPanel.init();
	if(idx == 0){
		self.tabPanel.insert(idx, mapPanel);
	}else{
		self.tabPanel.add(mapPanel);
	}
	self.tabPanel.setActiveTab(mapPanel);
	//mapPanel.on("OPEN_MAP", self.add_map, self);
},
*/
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
					{xtype: 'tbspacer', width: 50},
					"-",
					{text: "Flights", iconCls: "icoFlights", enableToggle: true, pressed: true},
					
					"-",
					{text: "Server Status", iconCls: "icoMpServers"},
					"-",
					//{text: "Settings", iconCls: "icoSettings"},
					//"-",
					{xtype: 'tbspacer', width: 50},
					"-",
					
					{text: "Now", iconCls: "icoRefresh",  handler: this.on_refresh_now, scope: this},
					{text: "Off", iconCls: "icoOn", pressed: true, enableToggle: true, scope: this,
						toggleGroup: "ref_rate", ref_rate: 0, toggleHandler: this.on_refresh_toggled},
					{text: "2", iconCls: "icoOff", enableToggle: true,   scope: this, width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 2, toggleHandler: this.on_refresh_toggled},
					{text: "3", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 3, toggleHandler: this.on_refresh_toggled},
					{text: "4", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 4, toggleHandler: this.on_refresh_toggled},
					{text: "5", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 5, toggleHandler: this.on_refresh_toggled},
					{text: "10", iconCls: "icoOff", enableToggle: true,   scope: this, width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 6, toggleHandler: this.on_refresh_toggled},
						
					"->",	
					"-",	
					{text: "Login", iconCls: "icoLogin"},
					"-",
					{text: "FGx", iconCls: "icoFgx", 
						menu: [
							{text: "Database Browser" }
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
	this.on_open_map("Main Map")
	
if(this.refresh_rate > 0){
	this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
}
},

//= Riggered for reshresh now
on_refresh_now: function(){
	this.store.load();
},


}) //< FGx.MainViewport
