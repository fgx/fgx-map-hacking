
Ext.namespace("FGx");

FGx.MainViewport = function(){

var self = this;	

var zooms = [1, 2, 3, 4, 5, 7, 9, 10, 20, 50, 73, 100, 150, 250];

	
this.centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);	
	


this.lblLat = new Ext.form.DisplayField({width: 100, value: "-"});
this.lblLon = new Ext.form.DisplayField({width: 100, value: "-"});

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

//============================================================
this.mapPanel = new GeoExt.MapPanel({
	
	frame: false,
	plain: true,
	border: 0,
	bodyBorder: false,
    region: "center",
        // we do not want all overlays, to try the OverlayLayerContainer
    map: new OpenLayers.Map({
		allOverlays: false,
		units: 'm',
		// this is the map projection here
		projection: new OpenLayers.Projection("EPSG:3857"),
		//sphericalMercator: true,
		
		// this is the display projection, I need that to show lon/lat in degrees and not in meters
		displayProjection: new OpenLayers.Projection("EPSG:4326"),
		
		// the resolutions are calculated by tilecache, when there is no resolution parameter but a bbox in
		// tilecache.cfg it shows you resolutions for all calculated zoomlevels in your browser: 
		// by http://yoururltothemap.org/tilecache.py/1.0.0/layername/ etc.
		// (This would not be necessary for 4326/900913 because this values are widely spread in
		// openlayer/osm/google threads, you will find the resolutions there)
		resolutions:RESOLUTIONS,
		
		// I set a max and min resolution, means setting available zoomlevels by default
		maxResolution: 156543.03390624999883584678,
		minResolution: 0.29858214169740676658,
		
		// i.e. maxExtent for EPSG 3572 is derived by browsing the very useful map at
		// http://nsidc.org/data/atlas/epsg_3572.html. I tried to get this values with mapnik2 and
		// proj4, but the values I get back with box2d are not very useful at the moment
		maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
		
		// zoomlevels 0-13 = 14 levels ?
		zoomLevels: 20
	}),
    center: this.centerpoint,
    zoom: 7,
	layers: LAYERS,
	
	/*
    layers: [
		
		new OpenLayers.Layer.WMS( "Natural Earth", 
			"http://map.fgx.ch:81/mapnik/fgxcache.py?", {
			layers: 'natural_earth_landmass', 
			format: 'image/png', 
			isBaselayer: true 
			}, {
				buffer:0,
				visibility: false
			}
		),
				
				
		// create a group layer (with several layers in the "layers" param)
		// to show how the LayerParamLoader works
		new OpenLayers.Layer.WMS("VFR",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?", {
				layers: [
					"VOR",
					"DME",
					"NDB",
					"FIX"
				],
				transparent: true,
				format: "image/png"
			}, {
				isBaseLayer: false,
				buffer: 0,
				// exclude this layer from layer container nodes
				displayInLayerSwitcher: false,
				visibility: false
			}
		),
		
		new OpenLayers.Layer.WMS("IFR",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?", {
				layers: [
					"ILS",
					"ILS_Info",
					"ILS_Marker"
					],
					transparent: true,
					format: "image/png"
				}, {
					isBaseLayer: false,
					buffer: 0,
					// exclude this layer from layer container nodes
					displayInLayerSwitcher: false,
					visibility: true
			}
		)
				
	], */
	
	/** Top Toolbar, these are all in butto groups */
	tbar: [
	
		/** Map Type  */
		{xtype: 'buttongroup',
            title: 'Settings', width: 80, id: "fgx-settings-box", 
            columns: 3,
            items: [
				{text: "Me", iconCls: "icoCallSign",  handler: this.on_me , tooltip: "My Settings", disabled: true},
				{text: "Map", toggleHandler: this.on_nav_toggled, iconCls: "icoMapCore", 
					menu: {
						items: [
							{text: "Landmass", group: "map_core", checked: true, xLayer: "landmass"},
							{text: "OSM - TODO", group: "map_core", checked: false, disabled: true, xLayer: "mapnick_gral"},
							{text: "OSM Light - TODO", group: "map_core", checked: false, disabled: true, xLayer: "mapnick_xgral"}
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
										{text: "Military Mode - only military and vortac", group: "map_mode", 
											checked: false, xCivMilMode: "military" , handler: this.on_civmil_mode},
										{text: "Both", group: "map_mode", 
											checked: false, xCivMilMode: "all", handler: this.on_civmil_mode}
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
				{xtype: "splitbutton", text: "VOR", pressed: true, enableToggle: true,  iconCls: "icoOn", navaid: "VOR", 
					toggleHandler: this.on_nav_toggled,
					menu: {
						items: [
							{text: "Show range", checked: false},
							{text: "Show FOO ", checked: true}
						]
					}
				},
				{text: "DME", enableToggle: true,  iconCls: "icoOff", navaid: "DME", toggleHandler: this.on_nav_toggled},
				{text: "NDB&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "NDB", toggleHandler: this.on_nav_toggled},
				{text: "Fix&nbsp;&nbsp;&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "FIX", toggleHandler: this.on_nav_toggled},
				{text: "VORTAC", enableToggle: true, iconCls: "icoOff", navaid: "NDB", toggleHandler: this.on_nav_toggled, 
					hidden: true, id: "fgx-vortac"}
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
	/****************************************************************************/
	/** Bottom Toolbar **/
	/****************************************************************************/
	bbar: [
		/** TODO Opacity Slider
		http://api.geoext.org/1.1/examples/layeropacityslider.html
		new GeoExt.LayerOpacitySlider({
			TODO_layer: "natural_earth_landmass",
			aggressive: true, 
			width: 200,
			isFormField: true,
			inverse: true,
			fieldLabel: "opacity",
			renderTo: "slider",
			plugins: new GeoExt.LayerOpacitySliderTip({template: '<div>Transparency: {opacity}%</div>'})
		}),
		*/
		{text: "Zoom:"},
		
		"->",
		{text: "TODO: Lat: "}, this.lblLat, 
		{text: "Lon: "},  this.lblLon
	
	]
}); //< mapPanel
this.mapPanel.map.events.register("mousemove", this.mapPanel.map, function(e) {      
    // @todo: make this proper lat/lon
	self.lblLat.setValue( e.x );
	self.lblLon.setValue( e.y );
    //OpenLayers.Util.getElement("tooltip").innerHTML = position 
});

//=================================================================================
// Other Widgets - Note the Map is passed in constructor as ref
//============================================================
this.flightsWidget = new FGx.FlightsWidget({mapPanel: this.mapPanel});

this.navWidget = new FGx.NavWidget({mapPanel: this.mapPanel});

//this.mapLayersTree = new FGx.MapLayersTree();


//=================================================================================
// Main Viewport auto rendered to body
//=================================================================================
this.viewport = new Ext.Viewport({
	layout: "border",
	frame: false,
	plain: true,
	border: 0,
	items: [

		this.mapPanel,
		{region: 'east', width: 400, 
			title: "FGx Map - Next Gen",
			xtype: 'tabpanel',
			frame: false,
			plain: true,
			border: 0,
			collapsible: true,
			activeItem: 0,
			items: [
				//this.mapLayersTree.tree,
				
				this.flightsWidget.grid,
				this.navWidget.grid
				
			]
        
		},
	]
});



this.flightsWidget.store.on("add", function(store, recs, idx){
	//console.log(recs);
	return;
	Ext.each(recs, function(rec){
		//var rec = recs[i];
		//console.log(rec.get("callsign"));
		// = show_radar (mcallsign, mlat, mlon, mheading, maltitude)
		//self.show_radar(rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("altitude"));
	}, this);
});
	
	
} //< FGx.MainViewport
