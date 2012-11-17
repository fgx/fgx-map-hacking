
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

this.flightsGrid.on("rowdblclick", function(grid, idx, e){
	//var callsign = self.flightsWidget.store.getAt(idx).get("callsign");
	//console.log(">>>>>>>>", callsign);
	//var existing_img = self.flightMarkersLayer.getFeatureBy("_callsign", callsign);
	//console.log("exist=", existing_img);
	//if(existing_img){
		//radarImageMarkers.removeFeatures(existing_img);
		//console.log("geom=", existing_img.geometry);
	var rec = self.flightsWidget.store.getAt(idx);
	 var pt = new OpenLayers.Geometry.Point(rec.get("lon"), rec.get("lat")
					).transform(this.displayProjection, this.map.getProjectionObject() );
	console.log(rec.get("lon"), rec.get("lat"), pt);
					
	this.map.setCenter( pt );
}, this);  


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
//==========================================================
// Shows aircraft on the RADAR map, with callsign (two features, poor openlayer)
this.DEADshow_radar = function show_radar(mcallsign, mlat, mlon, mheading, maltitude){

	// remove xisting iamge/label if exist
	/*
	var existing_img = radarImageMarkers.getFeatureBy("_callsign", mcallsign);
	if(existing_img){
		radarImageMarkers.removeFeatures(existing_img);
	}
	var existing_lbl  = radarLabelMarkers.getFeatureBy("_callsign", mcallsign);
	if(existing_lbl){
		radarLabelMarkers.removeFeatures(existing_lbl);
	}
	*/
	return;
	
	var pointImg = new OpenLayers.Geometry.Point(mlon, mlat
						).transform(this.displayProjection, this.map.getProjectionObject() );	
	if(!this.map.getExtent().containsPixel(pointImg, false)){
		//return; //alert(map.getExtent().containsLonLat(pointImg, false));
	}

	// Add Image
	var imgFeat = new OpenLayers.Feature.Vector(pointImg, {
				planerotation: mheading
				}); 
	imgFeat._callsign = mcallsign;
	this.flightMarkersLayer.addFeatures([imgFeat]);	
	//console.log(mcallsign, mlat, mlon, mheading, maltitude);
	
	var gxOff = 4;
	var gyOff = -8;

	var lxOff = 6;
	var lyOff = 2;
	
	// move the label offset
	if(mheading > 0  && mheading < 90){
		lyOff = lyOff - 15;
		gyOff = gyOff  + 15 ;
	}else if( mheading > 90 && mheading < 150){
		lyOff = lyOff + 5;
		gyOff = gyOff - 5;
	}else if( mheading > 270 && mheading < 360){
		lyOff = lyOff - 10;
		gyOff = gyOff  + 10;
		
	}

	// Add callsign label as separate feature, to have a background color (graphic) with offset
	var pointLabel = new OpenLayers.Geometry.Point(mlon, mlat
					).transform(this.displayProjection, this.map.getProjectionObject() );
	var lblFeat = new OpenLayers.Feature.Vector(pointLabel, {
                callsign: mcallsign,
				lxOff: lxOff, lyOff: lyOff,
				gxOff: gxOff, gyOff: gyOff
				});
	lblFeat._callsign = mcallsign;
	this.flightLabelsLayer.addFeatures([lblFeat]);	
	
}

/*
this.flightsStore.on("load", function(store, recs, idx){
	//console.log(recs.length);
	//return;
	this.flightLabelsLayer.removeAllFeatures();
	this.flightMarkersLayer.removeAllFeatures();
	recs_length = recs.length;
	for(var i = 0; i < recs_length; i++){
		var rec = recs[i];
		this.show_radar (rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("alt_ft") );
	};
}, this);
*/

//= Triggered when a refresh toolbar button is clicked
this.on_refresh_toggled = function(butt, checked){
	butt.setIconClass( checked ? "icoOn" : "icoOff");
	if(checked){
		this.runner.stopAll(); // stop if already ruinning
		this.refresh_rate = parseInt(butt.ref_rate, 10);
		if(this.refresh_rate === 0){
			//this.runner.stop()
		}else{
			this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
		}
	}
}

//= Riggered for reshresh now
this.on_refresh_now = function(){
	this.store.load();
}

this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
	
} //< FGx.MainViewport
