
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



//this.navWidget = new FGx.NavWidget({});


this.mpStatusGrid = new FGx.MpStatusGrid({flightsStore: this.flightsStore, title: "Server Status", closable: true});

//=================================================================================
// Main Viewport auto rendered to body
//=================================================================================

this.mapPanels = {};
this.mapPanels.base = new FGx.MapPanel({title: "Map 1", closable: false, flightsStore: this.flightsStore});
this.mapPanels.base.init();

//this.mapPanels.base2 = new FGx.MapPanel({title: "Map 2", closable: true, flightsStore: this.flightsStore});
//this.mapPanels.base2.init();

this.tabPanel = new Ext.TabPanel({
	region: "center",
	tabPosition: "top",
	frame: false, plain: true,
	activeItem: 0,
	items: [
		this.mapPanels.base,
		//this.mapPanels.base2,
		this.mpStatusGrid,
		this.flightsGrid
	]
	
});




this.viewport = new Ext.Viewport({
	layout: "border",
	frame: false,
	plain: true,
	border: 0,
	items: [

		//this.mapPanel,
		this.tabPanel
		,
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
