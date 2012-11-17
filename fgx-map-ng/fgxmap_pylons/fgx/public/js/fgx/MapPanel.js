

Ext.namespace("FGx");

FGx.MapPanel = Ext.extend(Ext.Panel, {

	
//var self = this;
get_display_projection: function(){
	if(!this.xDisplayProjection){
		this.xDisplayProjection = new OpenLayers.Projection("EPSG:4326");
	}
	return this.xDisplayProjection;
},
get_projection: function(){
	if(!this.xProjection){
		this.xProjection = OpenLayers.Projection("EPSG:3857");
	}
	return this.xProjection;
},

get_map: function(){
	if(!this.xMap){
		this.xMap =  new OpenLayers.Map({
			allOverlays: false,
			units: 'm',
			// this is the map projection here
			projection: this.get_projection(),
			//sphericalMercator: true,
			
			// this is the display projection, I need that to show lon/lat in degrees and not in meters
			displayProjection: this.get_display_projection(),
			
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


//======================================================
// Flights Grid
flights_grid: function(sto){
	if(!this.xFlightsGrid){
		
		this.xFlightsGrid =  new FGx.FlightsGrid({flightsStore: sto, title: "Flights", xHidden: true});
		
		this.xFlightsGrid.on("rowdblclick", function(grid, idx, e){

			var rec = grid.getStore().getAt(idx);
			var lonLat = new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")
				).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	
			this.get_map().setCenter( lonLat );
			this.get_map().zoomTo( 10 );
		}, this);  
				
	}
	return this.xFlightsGrid;
},

get_osm_dark: function(){
	if(!this.xOsmDark){
		this.xOsmDark = new OpenLayers.Layer.OSM.Mapnik( "Dark" );
		this.xOsmDark.setOpacity(0.5);	
	}
	return this.xOsmDark;
},

get_bookmark_button: function(){
		if(!this.xBookMarkButton){
		this.xBookMarkButton = new Ext.Button({
			text: "Bookmark",
			iconCls: "icoBookMarkAdd",
			scope: this,
			handler: function(){
				var d = new FGx.BookMarkDialog({bookmark_pk: 0});
				d.run_show();
				
			}
		});
		//this.xOsmDark.setOpacity(0.5);	
	}
	return this.xBookMarkButton;
},

//======================================================
// Create the Layers
get_layers: function(){
	

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
		this.get_osm_dark(),
		new OpenLayers.Layer.OSM.Mapnik( "OSM" ),
		
		new OpenLayers.Layer.WMS(
			"Landmass",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
				{layers: "natural_earth_landmass" , isBaselayer: "True", format: "image/png" 
				}, {  visibility: false}
		),
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
	
							{text: "Landmass", group: "map_core", checked: true, iconCls: "icoOff", pressed: false,
								xLayer: "ne_landmass", toggleHandler: this.on_base_layer, scope: this, toggleGroup: "xBaseLayer"
							},
							{text: "OSM", group: "map_core", checked: false, iconCls: "icoOff", pressed: false,
								xLayer: "osm_normal", toggleHandler: this.on_base_layer, scope: this, toggleGroup: "xBaseLayer"
							},
							{text: "Dark", group: "map_core", checked: false,  iconCls: "icoBlue", pressed: true,
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
					{xtype: 'buttongroup', 
						title: 'Utils', 
						columns: 2,
						items: [
							{text: "Goto", iconCls: "icoOff",
								menu: [
									{text: "Amsterdam", aptIdent: "EHAM", lat: 52.306, lon:4.7787 , 
										handler: this.on_goto, scope: this},
									{text: "London", aptIdent: "EGLL",  lat: 51.484, lon: -0.1510, 
										handler: this.on_goto, scope: this},
									{text: "Paris", aptIdent: "LFPG", lat: 48.994, lon: 2.650, 
										handler: this.on_goto, scope: this},
									{text: "San Fransisco", aptIdent: "KSFO", lat: 37.621302, lon: -122.371216, 
										handler: this.on_goto, scope: this},
									{text: "Zurich", aptIdent: "LSZH", lat: 47.467, lon: 8.5597, 
										handler: this.on_goto, scope: this},
								]
								
							},
							this.get_bookmark_button()
						]   
					}
					
				],
				
				//== Bottom Toolbar
				bbar: [

					{text: "Zoom", tooltip: "Click for default zoom"},
					new GeoExt.ZoomSlider({
						map: this.get_map(),
						aggressive: true,                                                                                                                                                   
						width: 150,
						plugins: new GeoExt.ZoomSliderTip({
							template: "<div>Zoom Level: {zoom}</div>"
						})
					}),
					"-",
					{text: "Opacity", tooltip: "Click for default zoom"},
					new GeoExt.LayerOpacitySlider({
						layer: this.get_osm_dark(),
						aggressive: true, 
						width: 150,
						isFormField: true,
						inverse: true,
						fieldLabel: "opacity",
						ssrenderTo: "slider",
						plugins: new GeoExt.LayerOpacitySliderTip({template: '<div>Transparency: {opacity}%</div>'})
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
				collapsed: false,
				activeItem: 0,
				items: [
					//this.mapLayersTree.tree,
					//this.flightsGrid,
					//this.flightsWidget.grid,
					//this.navWidget.grid
					this.flights_grid(config.flightsStore)
					
				]
			
			}
		]
		
		
	}, config);
	FGx.MapPanel.superclass.constructor.call(this, config);

	
}, // Constructor	

on_base_layer: function(butt, checked){
	//console.log(butt.xLayer);
	
	if(checked){
		this.set_base_layer(butt.text);
	}
	butt.setIconClass(checked ? "icoBlue" : "icoOff");
},

set_base_layer: function(layer_name){
	var layer = this.get_map().getLayersByName(layer_name)[0];
	//console.log(layer);
	this.get_map().setBaseLayer( layer );
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




init: function(){
	//console.log("INIT");
	
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
	this.get_map().addLayer( this.flightMarkersLayer );
	this.get_map().addLayer( this.flightLabelsLayer );
	
	this.set_base_layer("Dark"); //??? WTF!!
	
	this.flights_grid().getStore().on("load", function(store, recs, idx){
		//console.log("YESSSSS");
		this.flightLabelsLayer.removeAllFeatures();
		this.flightMarkersLayer.removeAllFeatures();
		var recs_length = recs.length;
		for(var i = 0; i < recs_length; i++){
			var rec = recs[i];
			this.show_radar (rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("alt_ft") );
		};
	}, this);
},



//==========================================================
// Shows aircraft on the RADAR map, with callsign (two features, poor openlayer)
show_radar: function show_radar(mcallsign, mlat, mlon, mheading, maltitude){

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
	//c//onsole.log(mcallsign, mlat, mlon, mheading, maltitude)
	var pointImg = new OpenLayers.Geometry.Point(mlon, mlat
						).transform(this.get_display_projection(), this.get_map().getProjectionObject() );	
	//if(!this.get_map().getExtent().containsPixel(pointImg, false)){
		//return; //alert(map.getExtent().containsLonLat(pointImg, false));
	//}

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
					).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	var lblFeat = new OpenLayers.Feature.Vector(pointLabel, {
                callsign: mcallsign,
				lxOff: lxOff, lyOff: lyOff,
				gxOff: gxOff, gyOff: gyOff
				});
	lblFeat._callsign = mcallsign;
	this.flightLabelsLayer.addFeatures([lblFeat]);	
	
},

on_goto: function(where){
	console.log(where.aptIdent);
	
	var lonLat = new OpenLayers.LonLat(where.lon, where.lat
			).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	
	this.get_map().setCenter( lonLat );
	this.get_map().zoomTo( 10 );
	//var pointLabel = new OpenLayers.Geometry.Point(mlon, mlat
	//				).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
					
	console.log(lonLat);
}


});
