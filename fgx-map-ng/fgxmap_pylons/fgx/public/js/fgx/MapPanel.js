

Ext.namespace("FGx");

FGx.MapPanel = Ext.extend(Ext.Panel, {

	
//var self = this;
						  
xDisplayProjection: new OpenLayers.Projection("EPSG:4326"),
xProjection: new OpenLayers.Projection("EPSG:3857"),

get_map: function(){
	if(!this.xMap){
		this.xMap =  new OpenLayers.Map({
			allOverlays: false,
			units: 'm',
			// this is the map projection here
			projection: this.xProjection,
			//sphericalMercator: true,
			
			// this is the display projection, I need that to show lon/lat in degrees and not in meters
			displayProjection: this.xDisplayProjection,
			
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
		//console.log("CREATED_map");
	}
	//console.log("get_map");
	return this.xMap;
},
lbl_lat: function(){
	if(!this.xLblLat){
		this.xLblLat =  new Ext.form.DisplayField({width: 100, value: "-"});
	}
	return this.xLblLat;
},
lbl_lon: function(){
	if(!this.xLblLon){
		this.xLblLon =  new Ext.form.DisplayField({width: 100, value: "-"});
	}
	return this.xLblLon;
},

flights_grid: function(){
	if(!this.xFlightsGrid){
		this.xFlightsGrid =  new Ext.Panel({title: "Foo"}); 
	}
	return this.xFlightsGrid;
},

get_layers: function(){
	
	var osm_light = new OpenLayers.Layer.OSM.Mapnik( "OSM Light" );
	osm_light.setOpacity(0.5);
	
	var LAYERS = [
		//=================================================
		// Overlay
		//=================================================
		new OpenLayers.Layer.WMS(
			"DME",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "DME" , transparent: "True" , format: "image/png"}, 
			{ visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"ILS Info",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "ILS_Info" , transparent: "True" , format: "image/png"}, 
			{visibility: false}
		),
		new OpenLayers.Layer.WMS(
		"Runway",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
				{layers: "Runway" , transparent: "True" , format: "image/png" 
				}, {  visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"NDB",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "NDB" , transparent: "True" , format: "image/png" 
			}, {  visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"ILS Marker",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "ILS_Marker" , transparent: "True" , format: "image/png" 
			}, {  visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"Airfield",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "Airfield" , transparent: "True" , format: "image/png" 
			}, {  visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"ILS",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "ILS" , transparent: "True" , format: "image/png" 
			}, {  visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"VOR",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "VOR" , transparent: "True" , format: "image/png" 
			}, {  visibility: false}
		),
		new OpenLayers.Layer.WMS(
			"FIX",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "FIX" , transparent: "True" , format: "image/png" 
			}, {  visibility: false}
		),
		/// Underlays
		new OpenLayers.Layer.WMS(
			"Landmass",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
				{layers: "natural_earth_landmass" , isBaselayer: "True", format: "image/png" 
				}, {  visibility: false}
		),
		new OpenLayers.Layer.OSM.Mapnik( "OSM Normal" ),
		osm_light
	];
	return LAYERS;
},

	
//===========================================================
//== CONSTRUCT
constructor: function(config) {
	
	config = Ext.apply({
		
		
		iconCls: "icoMap",
		frame: false, plain: true,border: 0,	bodyBorder: false,
		
		layout: "border",
		items: [
			{xtype: "gx_mappanel", region: "center",
				frame: false, plain: true, border: 0,	bodyBorder: false,
				map: this.get_map(),
				center:  new OpenLayers.LonLat(939262.20344,5938898.34882),
				zoom: 5,
				layers: this.get_layers(),
		
				tbar: [
				
					//== Map Type  
					{xtype: 'buttongroup', 
						title: 'Base Layer', width: 80, id: "fgx-settings-box", 
						columns: 3,
						items: [
	
							{text: "Landmass", group: "map_core", checked: true, iconCls: "icoOn", pressed: true,
								xLayer: "ne_landmass", toggleHandler: this.on_base_layer, scope: this, toggleGroup: "xBaseLayer"
							},
							{text: "OSM Normal", group: "map_core", checked: false, iconCls: "icoOff", pressed: false,
								xLayer: "osm_normal", toggleHandler: this.on_base_layer, scope: this, toggleGroup: "xBaseLayer"
							},
							{text: "OSM Light", group: "map_core", checked: false,  iconCls: "icoOff", pressed: false,
								xLayer: "osm_light", 
								toggleHandler: this.on_base_layer, scope: this, toggleGroup: "xBaseLayer"
							}
			
							
							
							/*
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
							} */
						]   
					},
					
					{xtype: 'buttongroup',
						title: 'Navigation Aids',
						columns: 5,
						items: [
							{xtype: "splitbutton", text: "VOR", pressed: false, enableToggle: true,  iconCls: "icoOff", navaid: "VOR", 
								toggleHandler: this.on_nav_toggled, scope: this,
								menu: {
									items: [
										{text: "Show range - TODO", checked: false, disabled: true}
									]
								}
							},
							{xtype: "splitbutton", text: "DME", enableToggle: true,  iconCls: "icoOff", navaid: "DME", 
								toggleHandler: this.on_nav_toggled,  scope: this,
								menu: {
									items: [
										{text: "Show range - TODO", checked: false, disabled: true}
									]
								}
							},
							{text: "NDB&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
								toggleHandler: this.on_nav_toggled, scope: this
							},
							{text: "Fix&nbsp;&nbsp;&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "FIX", 
								toggleHandler: this.on_nav_toggled, scope: this
							},
							{text: "VORTAC", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
								toggleHandler: this.on_nav_toggled, scope: this,
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
				
				//== Bottom Toolbar
				bbar: [

					{text: "Zoom:"},
					new GeoExt.ZoomSlider({
						map: this.get_map(),
						aggressive: true,                                                                                                                                                   
						width: 200,
						plugins: new GeoExt.ZoomSliderTip({
							template: "<div>Zoom Level: {zoom}</div>"
						})
					}),
					"->",
					{text: "TODO: Lat: "}, this.lbl_lat(), 
					{text: "Lon: "},  this.lbl_lon()
				
				]
			},
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
					//this.flightsGrid,
					//this.flightsWidget.grid,
					//this.navWidget.grid
					this.flights_grid()
					
				]
			
			}
		]
		
		
	}, config);
	FGx.MapPanel.superclass.constructor.call(this, config);

	
}, // Constructor	

on_base_layer: function(butt, checked){
	console.log(butt.xLayer);
	
	if(checked){
		var layer = this.xMap.getLayersByName(butt.text)[0];
		console.log(layer);
		this.xMap.setBaseLayer( layer );
	}
	butt.setIconClass(checked ? "icoOn" : "icoOff");
},

on_nav_toggled: function(butt, checked){
	butt.setIconClass( checked ? "icoOn" : "icoOff" );
	this.xMap.getLayersByName(butt.navaid)[0].setVisibility(checked);
},

on_apt_toggled: function(butt, checked){
 // TODO
 	butt.setIconClass( checked ? "icoOn" : "icoOff" );
},
on_civmil_mode: function(butt, checked){
 // TODO
	console.log(butt.xCivMilMode);
	var show_mil = butt.xCivMilMode != "civilian";
	//Ext.getCmp("fgx-vortac").setVisible( show_mil )
	//Ext.getCmp("fgx-mil-airports").setVisible( show_mil )
},

//get_info_panel: 


});
