

Ext.namespace("FGx");

FGx.MapPanel = Ext.extend(GeoExt.MapPanel, {

	
//var self = this;

xCenterPoint: new OpenLayers.LonLat(939262.20344,5938898.34882),
						  
xDisplayProjection: new OpenLayers.Projection("EPSG:4326"),
xProjection: new OpenLayers.Projection("EPSG:3857"),

xMap: new OpenLayers.Map({
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
}),
							
lblLat: new Ext.form.DisplayField({width: 100, value: "-"}),
lblLon: new Ext.form.DisplayField({width: 100, value: "-"}),

zoomSlider: new GeoExt.ZoomSlider({
	map: this.xMap,
	aggressive: true,                                                                                                                                                   
	width: 200,
	plugins: new GeoExt.ZoomSliderTip({
		template: "<div>Zoom Level: {zoom}</div>"
	})
}),
/*
BASE_LAYERS: {
	ne_landmass: new OpenLayers.Layer.WMS(
		"NE Landmass",
		"http://map.fgx.ch:81/mapnik/fgxcache.py?",
			{layers: "natural_earth_landmass" , isBaselayer: "True", format: "image/png" 
			}, {  visibility: false}
	),
	osm_normal: new OpenLayers.Layer.OSM.Mapnik( "OSM normal" ),
	osm_light: new OpenLayers.Layer.OSM.Mapnik( "OSM light" )
},
*/
//LAYERS.push(this.BASE_LAYERS.ne_landmass);


//this.BASE_LAYERS.osm_normal = new OpenLayers.Layer.OSM.Mapnik( "OSM normal" );
//this.BASE_LAYERS.osm_normal.setOpacity(1.0);
//LAYERS.push( this.BASE_LAYERS.osm_normal );


//this.BASE_LAYERS.osm_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
//this.BASE_LAYERS.osm_light.setOpacity(0.4);
//LAYERS.push( this.BASE_LAYERS.osm_light );
LAYERS: [
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
	new OpenLayers.Layer.OSM.Mapnik( "OSM Light" )
],

	
//===========================================================
//== Grid
constructor: function(config) {
	
	config = Ext.apply({
		sstitle: "Map",
		closable: true,
		iconCls: "icoMap",
		frame: false,
		plain: true,
		border: 0,
		bodyBorder: false,
		map: this.xMap,
		center: this.xCenterPoint,
		zoom: 5,
		layers: this.LAYERS,
		
		tbar: [
		
			//== Map Type  
			{xtype: 'buttongroup', 
				title: 'Settings', width: 80, id: "fgx-settings-box", 
				columns: 2,
				items: [
					//{text: "Me", iconCls: "icoCallSign",  
					//	handler: this.on_me , tooltip: "My Settings", disabled: true
					//},
					{text: "Map", iconCls: "icoMapCore", 
						menu: {
							items: [
								{text: "Landmass", group: "map_core", checked: true, 
									xLayer: "ne_landmass", handler: this.on_base_layer, scope: this
								},
								{text: "OSM Normal", group: "map_core", checked: false, 
									xLayer: "osm_normal", handler: this.on_base_layer, scope: this
								},
								{text: "OSM Light", group: "map_core", checked: false, 
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
			this.zoomSlider,
			"->",
			{text: "TODO: Lat: "}, this.lblLat, 
			{text: "Lon: "},  this.lblLon
		
		]
		
		
	}, config);
	FGx.MapPanel.superclass.constructor.call(this, config);
}, // Constructor	

on_base_layer: function(butt){
	console.log(butt.xLayer);
	var layer = this.xMap.getLayersByName(butt.text)[0];
	console.log(layer);
	this.xMap.setBaseLayer( layer );
	return;
	if( butt.xLayer == "ne_landmass"){
		this.xMap.setBaseLayer( this.BASE_LAYERS.ne_landmass );
		
	}else if ( butt.xLayer == "osm_normal"){
		this.xMap.setBaseLayer( this.BASE_LAYERS.osm_normal );
		
	}else if ( butt.xLayer == "osm_light"){
		this.xMap.setBaseLayer( this.BASE_LAYERS.osm_light );
	}
},

on_nav_toggled: function(butt, checked){
	butt.setIconClass( checked ? "icoOn" : "icoOff" );
	this.xMap.getLayersByName(butt.navaid)[0].setVisibility(checked);
},

on_apt_toggled: function(butt, checked){
 // TODO	
},
on_civmil_mode: function(butt, checked){
 // TODO	
}


});

/*
	this.xMap = new OpenLayers.Map({
			allOverlays: false,
			units: 'm',
			// this is the map projection here
			projection: xProjection,
			//sphericalMercator: true,
			
			// this is the display projection, I need that to show lon/lat in degrees and not in meters
			displayProjection: xDisplayProjection,
			
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
/*
	var LAYERS = [];
	//=================================================
	// Overlay
	//=================================================
	LAYERS.push( new OpenLayers.Layer.WMS(
	"DME",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "DME" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"ILS Info",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "ILS_Info" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"Runway",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "Runway" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"NDB",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "NDB" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"ILS Marker",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "ILS_Marker" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"Airfield",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "Airfield" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"ILS",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "ILS" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));
	LAYERS.push( new OpenLayers.Layer.WMS(
	"VOR",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "VOR" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));

	LAYERS.push( new OpenLayers.Layer.WMS(
	"FIX",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "FIX" , transparent: "True" , format: "image/png" 
		}, {  visibility: false}
	));


	//=================================================
	// Underlay
	//=================================================
	this.BASE_LAYERS = {};
	this.BASE_LAYERS.ne_landmass = new OpenLayers.Layer.WMS(
	"NE Landmass",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
		{layers: "natural_earth_landmass" , isBaselayer: "True", format: "image/png" 
		}, {  visibility: false}
	);
	LAYERS.push(this.BASE_LAYERS.ne_landmass);

	
	this.BASE_LAYERS.osm_normal = new OpenLayers.Layer.OSM.Mapnik( "OSM normal" );
	this.BASE_LAYERS.osm_normal.setOpacity(1.0);
	LAYERS.push( this.BASE_LAYERS.osm_normal );


	this.BASE_LAYERS.osm_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
	this.BASE_LAYERS.osm_light.setOpacity(0.4);
	LAYERS.push( this.BASE_LAYERS.osm_light );

	*/
/*

		
	
	


	
	

	FGx.MapPanel.superclass.constructor.call(this, {
		title: "Map",
		closable: true,
		iconCls: "icoMap",
		frame: false,
		plain: true,
		border: 0,
		bodyBorder: false,
		map: this.xMap,
		center: xCenterPoint,
		zoom: 5,
		layers: LAYERS,
		
		tbar: [
		
			//== Map Type  
			{xtype: 'buttongroup', 
				title: 'Settings', width: 80, id: "fgx-settings-box", 
				columns: 2,
				items: [
					//{text: "Me", iconCls: "icoCallSign",  
					//	handler: this.on_me , tooltip: "My Settings", disabled: true
					//},
					{text: "Map", iconCls: "icoMapCore", 
						menu: {
							items: [
								{text: "Landmass", group: "map_core", checked: true, xLayer: "ne_landmass",
									handler: on_base_layer
								},
								{text: "OSM Normal", group: "map_core", checked: false, 
									xLayer: "osm_normal", handler: on_base_layer
								},
								{text: "OSM Light", group: "map_core", checked: false, 
									xLayer: "osm_light", 
									handler: on_base_layer
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
						toggleHandler: on_nav_toggled,
						menu: {
							items: [
								{text: "Show range - TODO", checked: false, disabled: true}
							]
						}
					},
					{xtype: "splitbutton", text: "DME", enableToggle: true,  iconCls: "icoOff", navaid: "DME", 
						toggleHandler: on_nav_toggled, 
						menu: {
							items: [
								{text: "Show range - TODO", checked: false, disabled: true}
							]
						}
					},
					{text: "NDB&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
						toggleHandler: on_nav_toggled
					},
					{text: "Fix&nbsp;&nbsp;&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "FIX", 
						toggleHandler: on_nav_toggled
					},
					{text: "VORTAC", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
						toggleHandler: on_nav_toggled, 
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
			this.zoomSlider,
			"->",
			{text: "TODO: Lat: "}, lblLat, 
			{text: "Lon: "},  lblLon
		
		]
	});
	
	
	
	
} /// end MapPanel 

Ext.extend(FGx.MapPanel,GeoExt.MapPanel, {
	initComponent: function(){
		FGx.MapPanel.superclass.initComponent.apply(this, arguments);
	},
	onRender: function(){
		FGx.MapPanel.superclass.onRender.apply(this, arguments);
	},
});
*/