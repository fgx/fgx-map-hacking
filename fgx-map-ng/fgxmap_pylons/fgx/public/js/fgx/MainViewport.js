
Ext.namespace("FGx");

FGx.MainViewport = function(){

var self = this;	

var zooms = [1, 2, 3, 4, 5, 7, 9, 10, 20, 50, 73, 100, 150, 250];
this.centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);	
	

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


this.runner = new Ext.util.TaskRunner();


//===========================================================================
//= Layers
//===========================================================================
this.flightMarkersLayer = new OpenLayers.Layer.Vector(
	"Radar Markers", 
	{styleMap: new OpenLayers.StyleMap({
			"default": {
				strokeColor: "lime",
				strokeWidth: 1,
				fillColor: "lime",

				externalGraphic: "/images/radar_blip2.png",
				graphicWidth: 8,
				graphicHeight: 24,
				graphicOpacity: 1,
				graphicXOffset: 0,
				graphicYOffset: -20,
				
				fontColor: "black",
				fontSize: "12px",
				fontFamily: "Helvetica, Arial, sans-serif",
				fontWeight: "bold",
				rotation : "${planerotation}",
			},
			"select": {
				fillColor: "black",
				strokeColor: "yellow",
				pointRadius: 12,
				fillOpacity: 1,
			}
		})
	}, {  visibility: true}
)

this.flightLabelsLayer =  new OpenLayers.Layer.Vector(
	"Radar Label", 
	{
		styleMap:  new OpenLayers.StyleMap({
			"default": {
				fill: true,
				fillOpacity: 1,
				fillColor: "black",
				strokeColor: "green",
				strokeWidth: 1,

				//graphic: false,
				externalGraphic: "/images/fgx-background-black.png",
				graphicWidth: 50,
				graphicHeight: 12,
				graphicOpacity: 0.8,
				graphicXOffset: "${gxOff}",
				graphicYOffset: "${gyOff}",
				
				
				fontColor: "white",
				fontSize: "10px",
				fontFamily: "sans-serif",
				fontWeight: "bold",
				labelAlign: "left",
				labelXOffset: "${lxOff}", 
				labelYOffset: "${lyOff}", 
				label : "${callsign}",
				//rotation : "${planerotation}",

			},
			"select": {
				fillColor: "black",
				strokeColor: "yellow",
				pointRadius: 12,
				fillOpacity: 1,
			}

		})
	}
);


this.get_layers = function(){
	LAYERS.push( this.flightMarkersLayer );
	LAYERS.push( this.flightLabelsLayer );
	return LAYERS;	
}





//===========================================================================
//= Handlers
//===========================================================================
this.on_nav_toggled = function(butt, checked){
	// @todo:
	//console.log(butt, checked, butt.navaid);
	butt.setIconClass( checked ? "icoOn" : "icoOff" );
	self.mapPanel.map.getLayersByName(butt.navaid)[0].setVisibility(checked);
	
}
this.on_apt_toggled = function(butt, checked){
	// @todo:
	//console.log(butt, checked, butt.apt);
	butt.setIconClass( checked ? "icoOn" : "icoOff" );
	
}

this.on_civmil_mode = function(butt){
	console.log(butt.xCivMilMode);
	var show_mil = butt.xCivMilMode != "civilian";
	Ext.getCmp("fgx-vortac").setVisible( show_mil )
	Ext.getCmp("fgx-mil-airports").setVisible( show_mil )
}


this.on_me = function(){
	FGx.msg("Yes", "it works");
	alert("TODO, this will allow custom settings");
}

//===========================================================================
//= Map Setup
//===========================================================================

/*
this.displayProjection = new OpenLayers.Projection("EPSG:4326"),
this.projection = new OpenLayers.Projection("EPSG:3857")
*/
/*
this.map = new OpenLayers.Map({
		allOverlays: false,
		units: 'm',
		// this is the map projection here
		projection: this.projection,
		//sphericalMercator: true,
		
		// this is the display projection, I need that to show lon/lat in degrees and not in meters
		displayProjection: this.displayProjection,
		
		// the resolutions are calculated by tilecache, when there is no resolution parameter but a bbox in
		// tilecache.cfg it shows you resolutions for all calculated zoomlevels in your browser: 
		// by http://yoururltothemap.org/tilecache.py/1.0.0/layername/ etc.
		// (This would not be necessary for 4326/900913 because this values are widely spread in
		// openlayer/osm/google threads, you will find the resolutions there)
		resolutions: RESOLUTIONS,
		
		// I set a max and min resolution, means setting available zoomlevels by default
		maxResolution: 156543.03390624999883584678,
		minResolution: 0.29858214169740676658,
		
		// i.e. maxExtent for EPSG 3572 is derived by browsing the very useful map at
		// http://nsidc.org/data/atlas/epsg_3572.html. I tried to get this values with mapnik2 and
		// proj4, but the values I get back with box2d are not very useful at the moment
		maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
		
		// zoomlevels 0-13 = 14 levels ?
		zoomLevels: 20
});
*/

//============================================================
// mapPanel - geoExt
//============================================================
/*
this.lblLat = new Ext.form.DisplayField({width: 100, value: "-"});
this.lblLon = new Ext.form.DisplayField({width: 100, value: "-"});

this.zoomSlider = new GeoExt.ZoomSlider({
	map: this.map,
	aggressive: true,                                                                                                                                                   
	width: 200,
	plugins: new GeoExt.ZoomSliderTip({
		template: "<div>Zoom Level: {zoom}</div>"
	})
});


this.on_base_layer = function(butt){
	if( butt.xLayer == "ne_landmass"){
		this.map.setBaseLayer( BASE_LAYERS.ne_landmass );
		
	}else if ( butt.xLayer == "osm_normal"){
		this.map.setBaseLayer( BASE_LAYERS.osm_normal );
		
	}else if ( butt.xLayer == "osm_light"){
		this.map.setBaseLayer( BASE_LAYERS.osm_light );
	}
}
*/
/*
this.mapPanel = new GeoExt.MapPanel({
	
	frame: false,
	plain: true,
	border: 0,
	bodyBorder: false,
    region: "center",
        // we do not want all overlays, to try the OverlayLayerContainer
    map: this.map,
    center: this.centerpoint,
    zoom: 5,
	layers: this.get_layers(),
	
	/// Top Toolbar, these are all in button groups
	tbar: [
	
		//== Map Type  
		{xtype: 'buttongroup', 
            title: 'Settings', width: 80, id: "fgx-settings-box", 
            columns: 2,
            items: [
				//{text: "Me", iconCls: "icoCallSign",  
				//	handler: this.on_me , tooltip: "My Settings", disabled: true
				//},
				{text: "Map", toggleHandler: this.on_nav_toggled, iconCls: "icoMapCore", 
					menu: {
						items: [
							{text: "Landmass", group: "map_core", checked: false, xLayer: "ne_landmass",
								handler: this.on_base_layer, scope: this
							},
							{text: "OSM Normal", group: "map_core", checked: false, 
								xLayer: "osm_normal", handler: this.on_base_layer, scope: this
							},
							{text: "OSM Light", group: "map_core", checked: true, 
								xLayer: "osm_light", 
								handler: this.on_base_layer, scope: this
							}
						]
					}
				},
				{iconCls: "icoSettings", 
					menu: {
						items: [
							{text: "Mode" ,
								menu: {
									items: [
										{text: "Civilian mode - no military AF or vortac", group: "map_mode", 
											checked: true, xCivMilMode: "civilian", handler: this.on_civmil_mode},
										{text: "Military Mode - only military and vortac - TODO", group: "map_mode", 
											checked: false, xCivMilMode: "military", disabled: true,
											handler: this.on_civmil_mode
										},
										{text: "Both - TODO", group: "map_mode", 
											checked: false, xCivMilMode: "all", disabled: true,
											handler: this.on_civmil_mode
										}
									]
								}
							}
						]
					}
				} 
            ]   
		},
		
		{xtype: 'buttongroup',
            title: 'Navigation Aids',
            columns: 5,
            items: [
				{xtype: "splitbutton", text: "VOR", pressed: false, enableToggle: true,  iconCls: "icoOff", navaid: "VOR", 
					toggleHandler: this.on_nav_toggled,
					menu: {
						items: [
							{text: "Show range - TODO", checked: false, disabled: true}
						]
					}
				},
				{xtype: "splitbutton", text: "DME", enableToggle: true,  iconCls: "icoOff", navaid: "DME", 
					toggleHandler: this.on_nav_toggled,
					menu: {
						items: [
							{text: "Show range - TODO", checked: false, disabled: true}
						]
					}
				},
				{text: "NDB&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
					toggleHandler: this.on_nav_toggled
				},
				{text: "Fix&nbsp;&nbsp;&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "FIX", 
					toggleHandler: this.on_nav_toggled
				},
				{text: "VORTAC", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
					toggleHandler: this.on_nav_toggled, 
					hidden: true, id: "fgx-vortac"
				}
            ]   
		},
		{xtype: 'buttongroup', disabled: true,
            title: 'Airports - TODO', 
            columns: 6,
            items: [
				{text: "Major", enableToggle: true, pressed: true, iconCls: "icoOn", apt: "major", toggleHandler: this.on_apt_toggled},
				{text: "Minor", enableToggle: true, iconCls: "icoOff", apt: "minor", toggleHandler: this.on_apt_toggled},
				{text: "Small", enableToggle: true, iconCls: "icoOff", apt: "small", toggleHandler: this.on_apt_toggled},
				{text: "Military", enableToggle: true, iconCls: "icoOff", apt: "military", toggleHandler: this.on_apt_toggled,
					hidden: true, id: "fgx-mil-airports"},
				{text: "Seaports", enableToggle: true, iconCls: "icoOff", apt: "seaports", toggleHandler: this.on_apt_toggled},
				{text: "Heliports", enableToggle: true, iconCls: "icoOff", apt: "heliports", toggleHandler: this.on_apt_toggled},
            ]   
		},		
		"->",
		
	],
	
	///========================================
	//== Bottom Toolbar 
	bbar: [

		{text: "Zoom:"},
		this.zoomSlider,
		"->",
		{text: "TODO: Lat: "}, this.lblLat, 
		{text: "Lon: "},  this.lblLon
	
	]
}); //< mapPanel
this.mapPanel.map.events.register("mousemove", this.mapPanel.map, function(e) {      
    // @todo: make this proper lat/lon
   // console.log(e);
	var pixel = new OpenLayers.Pixel(e.xy.x,e.xy.y);
	var lonlat = self.map.getLonLatFromPixel(pixel);
    //var pt = new OpenLayers.Geometry.Point(e.x,  e.y
	//		).transform(self.map.getProjectionObject(), self.displayProjection);
	
	//self.lblLat.setValue( pt.x );
	//self.lblLon.setValue( pt.y );
	self.lblLat.setValue( lonlat.lat );
	self.lblLon.setValue( lonlat.lon );
    //OpenLayers.Util.getElement("tooltip").innerHTML = position 
});
*/

//=================================================================================
// Other Widgets - Note the Map is passed in constructor as ref
//============================================================
//this.flightsWidget = new FGx.FlightsWidget({});
this.flightsGrid = new FGx.FlightsGrid({store: this.flightsStore, title: "Flights", closable: true});

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


this.navWidget = new FGx.NavWidget({});

//this.mapLayersTree = new FGx.MapLayersTree();


//=================================================================================
// Main Viewport auto rendered to body
//=================================================================================

this.mapPanels = {};
this.mapPanels.base = new FGx.MapPanel({title: "map1"});
this.mapPanels.base2 = new FGx.MapPanel({title: "map2"});

this.tabPanel = new Ext.TabPanel({
	region: "center",
	tabPosition: "top",
	frame: false, plain: true,
	activeItem: 0,
	items: [
		this.mapPanels.base,
		this.mapPanels.base2,
		this.flightsGrid,
		
		//
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
this.show_radar = function show_radar(mcallsign, mlat, mlon, mheading, maltitude){

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


	
} //< FGx.MainViewport
