
Ext.namespace("FGx");

FGx.MainViewport = function(){

var self = this;	

var zooms = [1, 2, 3, 4, 5, 7, 9, 10, 20, 50, 73, 100, 150, 250];
//this.centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);	
	

//===========================================================
//== FlightsStore
this.flightsStore = new Ext.data.JsonStore({
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
	autoLoad: true,
});

this.update_flights = function(){
	self.flightsStore.load();
}

this.refresh_rate = 2;
this.runner = new Ext.util.TaskRunner();







//=================================================================================
// Other Widgets - Note the Map is passed in constructor as ref
//============================================================
//this.flightsWidget = new FGx.FlightsWidget({});
this.flightsGrid = new FGx.FlightsGrid({
	flightsStore: this.flightsStore, 
	title: "Flights", 
	closable: true,
	xHidden: false
});



this.settingsWidget = new FGx.SettingsWidget({runner: this.runner});
this.settingsWidget.on("SET_REFRESH", function(rate){
	//console.log("SET_REFRESH", rate);
	this.runner.stopAll(); // stop if already running
	this.refresh_rate = rate;
	if(this.refresh_rate === 0){
		//this.runner.stop()
	}else{
		this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
	}
}, this);


this.mpStatusGrid = new FGx.MpStatusGrid({flightsStore: this.flightsStore, title: "Server Status"});

//=================================================================================
// Map Panels
//=================================================================================

this.on_open_map = function(lonLat, zoom, title){
	var newMap = new FGx.MapPanel({
		title: title, closable: true, 
		flightsStore: self.flightsStore,
		lonLat: lonLat, zoom: zoom
	});
	console.log(self.flightsStore);
	//newMap.on("OPEN_MAP", function(lonLat, zoom, title){
	///	this.on_open_map(lonLat, zoom, title);
	//, this);
	this.tabPanel.add(newMap);
	this.tabPanel.setActiveTab(newMap);
	
};



//this.mapPanels.mainMap.init();
//this.mapPanels.mainMap.on("OPEN_MAP", this.on_open_map, this);
	


//this.mapPanels.base2 = new FGx.MapPanel({title: "Map 2", closable: true, flightsStore: this.flightsStore});
//this.mapPanels.base2.init();

this.tabPanel = new Ext.TabPanel({
	region: "center",
	tabPosition: "top",
	frame: false, plain: true,
	activeItem: 0,
	items: [
		
		//this.mapPanels.mainMap,
		//this.mapPanels.base2,
		
		this.flightsGrid,
		this.mpStatusGrid,
		this.settingsWidget
	]
	
});

//this.mapPanels = {};
this.add_map = function(title, closable, lonLat, zoom, idx){
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
	mapPanel.on("OPEN_MAP", self.add_map, self);
}

this.add_map("Main Map", false, false, false, 0);



this.viewport = new Ext.Viewport({
	layout: "border",
	frame: false,
	plain: true,
	border: 0,
	items: [

		//this.mapPanel,
		this.tabPanel
		/*
		{xtype: "panel",
			region: "west",
			collapsible: true,
			width: 200,
			title: "Options",
			tbar: [
				{xtype: 'buttongroup',
					title: 'Refresh Secs',
					columns: 7,
					items: [
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
							toggleGroup: "ref_rate", ref_rate: 6, toggleHandler: this.on_refresh_toggled}
					]   
				}
				
			]
		}
		*/
		/* {region: 'east', width: 400, 
			title: "FGx Map - Next Gen",
			xtype: 'tabpanel',
			frame: false,
			plain: true,
			border: 0,
			collapsible: true,
			activeItem: 0,
			items: [
				//this.mapLayersTree.tree,
				this.flightsGrid,
				//this.flightsWidget.grid,
				this.navWidget.grid
				
			]
        
		},
		*/
	]
});


this.initialize = function(){
	//self.map.setBaseLayer( BASE_LAYERS.osm_light );	
}

//= Riggered for reshresh now
this.on_refresh_now = function(){
	this.store.load();
}

this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
	
} //< FGx.MainViewport
