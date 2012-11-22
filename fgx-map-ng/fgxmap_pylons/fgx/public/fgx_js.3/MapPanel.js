

Ext.namespace("FGx");

FGx.MapPanel = Ext.extend(GeoExt.MapPanel, {

L: {},

get_display_projection: function(){
	return new OpenLayers.Projection("EPSG:4326");
},

get_graticule: function(){
	if(!this.xGraticule){
		this.xGraticule =	new OpenLayers.Control.Graticule({
			numPoints: 1, 
			autoActivate: false,
			labelled: true,
			lineSymbolizer:{strokeColor: "grey", strokeWidth: 1, strokeOpacity: 0.3},
			// WTF below dont work !
			labelSymbolizer:{strokeColor: "red", strokeWidth: 1, strokeOpacity: 0.5}
		});
	}
	return this.xGraticule;
},

get_map: function(){
	if(!this.xMap){
		this.xMap =  new OpenLayers.Map({
			allOverlays: false,
			units: 'm',
			// this is the map projection here
			projection: new OpenLayers.Projection("EPSG:3857"), // this.get_projection(),
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
		this.xMap.addControl( this.get_graticule() );
		this.xMap.events.register("mousemove", this, function (e) {
			var pos = this.get_map().getLonLatFromViewPortPx(e.xy		
				).transform(this.get_display_projection(), this.get_map().getProjectionObject() );
			// TODO make sense
			//var lonLat = new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")
			//	).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
			this.lbl_lat().setValue(pos.lat);
			this.lbl_lon().setValue(pos.lon);
		});
	}
	return this.xMap;
},


//======================================================
//=== LatLon Labels
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



get_osm_lite: function(){
	if(!this.L.lite){
		this.L.lite = new OpenLayers.Layer.OSM.Mapnik( "Light" );
		this.L.lite.setOpacity(0.4);	
	}
	return this.L.lite;
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
	this.L.blip = new OpenLayers.Layer.Vector("HighLight Markers");
	this.L.track = new OpenLayers.Layer.Vector("Track Lines Layer");	
	this.L.fpline = new OpenLayers.Layer.Vector("Flight Plan Line");
	this.L.fplbl = new OpenLayers.Layer.Vector("Flight Plan Labels", 
			{
                styleMap: new OpenLayers.StyleMap({'default':{
                    strokeColor: "black",
                    strokeOpacity: 1,
                    strokeWidth: 3,
                    fillColor: "#FF5500",
                    fillOpacity: 0.5,
                    pointRadius: 6,
                    pointerEvents: "visiblePainted",
                    // label with \n linebreaks
                    label : "${ident}",
                    
                    fontColor: "red",
                    fontSize: "12px",
                    fontFamily: "Courier New, monospace",
                    fontWeight: "bold",
                    labelAlign: "${align}",
                    labelXOffset: "${xOffset}",
                    labelYOffset: "${yOffset}",
                    labelOutlineColor: "white",
                    labelOutlineWidth: 3
                }})
                //renderers: renderer
            }
	);
	
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
		this.get_osm_lite(),
		new OpenLayers.Layer.OSM.Mapnik( "OSM" ),
		
		new OpenLayers.Layer.WMS(
			"Landmass",
			"http://map.fgx.ch:81/mapnik/fgxcache.py?",
				{layers: "natural_earth_landmass" , isBaselayer: "True", format: "image/png" 
				}, {  visibility: false}
		),
		this.L.blip,
		this.L.track,
		//this.flightPlanLayer,
		this.L.fplbl,
		this.L.fpline
		
	];
	return LAYERS;
},

get_store: function(){
	
	if(!this.xFlightsStore){
		this.xFlightsStore = Ext.StoreMgr.lookup("flights_store");
		this.xFlightsStore.on("load", function(sto, recs){
			//console.log("YES");
			this.flightLabelsLayer.removeAllFeatures();
			this.flightMarkersLayer.removeAllFeatures();
			var rec_len = recs.length;
			for(var i=0; i< recs.length; i++){
				var r = recs[i].data;
				this.show_radar(r.callsign, r.lat, r.lon, r.hdg, r.altitude);
			}
		}, this);
	}
	return this.xFlightsStore;
},
	
//===========================================================
//== CONSTRUCT
constructor: function(config) {
	
	//console.log("constr", config.title, config.lat, config.lon);
	
	var ll;
	if(config.lat || config.lon){
		ll =  new OpenLayers.Geometry.Point(config.lon, config.lat
			).transform(this.get_display_projection(), this.get_map().getProjectionObject() ); 
		ll.xFlag = "New";
	}else{
		ll = new OpenLayers.LonLat(939262.20344, 5938898.34882);
		ll.xFlag = "Default"
	}
	//console.log(ll.xFlag, ll.x, ll.y);
	config = Ext.apply({
		
		fgxType: "MapPanel",
		iconCls: "icoMap",
		frame: false, plain: true,border: 0,	bodyBorder: false,
		
		map: this.get_map(),
		center:  ll, 
		zoom: config.zoom ? config.zoom : 5,
		layers: this.get_layers(),
		xxxFlightsStore: this.get_store(),
		tbar: [
		
			//== Map Type  
			{xtype: 'buttongroup', 
				title: 'Base Layer',
				columns: 1,
				items: [
					{text: "Light", iconCls: "icoYellow", width: 90, 
						id: this.getId() + "map-base-button",
						menu: [
							{text: "Outline", group: "map_core", checked: false, xiconCls: "icoBlue",
								xLayer: "Landmass", handler: this.on_base_layer, scope: this, group: "xBaseLayer"
							},
							{text: "Normal", group: "map_core", checked: false, xiconCls: "icoGreen",
								xLayer: "OSM", handler: this.on_base_layer, scope: this, group: "xBaseLayer"
							},
							{text: "Light", group: "map_core", checked: true,  xiconCls: "icoYellow",
								xLayer: "Light", 
								handler: this.on_base_layer, scope: this, group: "xBaseLayer"
							}
						]
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
					}
					//{text: "VORTAC", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
					//	toggleHandler: this.on_nav_toggled, scope: this,
					//	hidden: true, id: "fgx-vortac"
					//}
				]   
			},
			{xtype: 'buttongroup', disabled: true,
				title: 'Airports - TODO', 
				columns: 6,
				items: [
					{text: "Major", enableToggle: true, pressed: true, iconCls: "icoOn", apt: "major", toggleHandler: this.on_apt_toggled},
					{text: "Minor", enableToggle: true, iconCls: "icoOff", apt: "minor", toggleHandler: this.on_apt_toggled},
					{text: "Small", enableToggle: true, iconCls: "icoOff", apt: "small", toggleHandler: this.on_apt_toggled},
					//{text: "Military", enableToggle: true, iconCls: "icoOff", apt: "military", toggleHandler: this.on_apt_toggled,
					//	hidden: true, id: "fgx-mil-airports"},
					{text: "Seaports", enableToggle: true, iconCls: "icoOff", apt: "seaports", toggleHandler: this.on_apt_toggled},
					{text: "Heliports", enableToggle: true, iconCls: "icoOff", apt: "heliports", toggleHandler: this.on_apt_toggled},
				]   
			},
			{xtype: 'buttongroup', 
				title: 'Utils', 
				columns: 2,
				items: [
					this.get_bookmark_button()
				]
			}
		],
		
		//== Bottom Toolbar
		bbar: [

			{text: "Zoom", tooltip: "Click for default zoom",
				zoom: 4, handler: this.on_zoom_to, scope: this
			},
			new GeoExt.ZoomSlider({
				map: this.get_map(),
				aggressive: true,                                                                                                                                                   
				width: 100,
				plugins: new GeoExt.ZoomSliderTip({
					template: "<div>Zoom Level: {zoom}</div>"
				})
			}),
			{text: "100", zoom: 6, handler: this.on_zoom_to, scope: this},
			{text: "30", zoom: 10, handler: this.on_zoom_to, scope: this},
			{text: "10", zoom: 14, handler: this.on_zoom_to, scope: this},
			{text: "&nbsp;5&nbsp;", zoom: 16, handler: this.on_zoom_to, scope: this},
			{text: "&nbsp;2&nbsp;",  zoom: 17, handler: this.on_zoom_to, scope: this},
			"-",
			{text: "Opacity", tooltip: "Click for default opacity"},
			new GeoExt.LayerOpacitySlider({
				layer: this.get_osm_lite(),
				aggressive: true, 
				width: 80,
				isFormField: true,
				inverse: true,
				fieldLabel: "opacity",
				ssrenderTo: "slider",
				plugins: new GeoExt.LayerOpacitySliderTip({template: '<div>Transparency: {opacity}%</div>'})
			}),
			"-",
			{text: "Graticule", iconCls: "icoOff", enableToggle: true, pressed: false,
				scope: this, 
				toggleHandler: function(butt, checked){
					if(checked){
						this.get_graticule().activate();
					}else{
						this.get_graticule().deactivate();
					}
				}
			},
			"-",
			"->",
			{text: "TODO: Lat: "}, this.lbl_lat(), 
			{text: "Lon: "},  this.lbl_lon(),
			"-",
			{text: "DEV", scope: this,
				handler: function(){
					console.log(this.get_map().getExtent())
				}
			}
		
		]
	
	}, config);
	FGx.MapPanel.superclass.constructor.call(this, config);

	
}, // Constructor	

on_base_layer: function(butt, checked){
	console.log(butt.xLayer);
	var bbButton = Ext.getCmp( this.getId() + "map-base-button");
	//if(checked){
	this.set_base_layer(butt.xLayer);
	//}
	bbButton.setIconClass(butt.xiconCls);
	bbButton.setText(butt.text);
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


on_zoom_to: function(butt){
	this.get_map().zoomTo( butt.zoom );
},

init: function(){

	
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

on_goto: function(butt){
	//var lonLat = new OpenLayers.LonLat(butt.lon, butt.lat
	//		).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	this.fireEvent("OPEN_MAP", butt.text, true, butt.lon, butt.lat, butt.zoom);
},

load_tracker: function(tracks){
	
	this.trackLinesLayer.removeAllFeatures();
	var trk_length = tracks.length;
	var points = [];
	//var points;
	var p;
	for(var i =0; i < trk_length; i++){
		p = tracks[i];
		points.push(
				new OpenLayers.Geometry.Point(p.lon, p.lat
					).transform(this.get_display_projection(),  this.get_map().getProjectionObject() )
			  );
	}
	var line = new OpenLayers.Geometry.LineString(points);

	var style = { 
		strokeColor: '#0000ff', 
		strokeOpacity: 0.5,
		strokeWidth: 2
	};

	//var lineFeature = new OpenLayers.Feature.Vector(line, null, style);
	this.trackLinesLayer.addFeatures([ new OpenLayers.Feature.Vector(line, null, style) ]);
	this.get_map().zoomToExtent(this.trackLinesLayer.getDataExtent()); 
	this.get_map().zoomOut();
	
},

load_flight_plan: function(recs){
	//console.log("FP", recs);
	this.fpLineLayer.removeAllFeatures();
	this.fpLabelsLayer.removeAllFeatures();
	
	var lenny = recs.length;
	var fpoints = [];
	var idx_dic = {};
	var navLabels = [];
	for(var i = 0; i < lenny; i++){
		var r = recs[i].data;
		if(r.lat && r.lon){
			var navPt = new OpenLayers.Geometry.Point(r.lon, r.lat
					).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
			var lbl = new OpenLayers.Feature.Vector(navPt);
			lbl.attributes = r;
			navLabels.push(lbl);
			//this.fpLabelsLayer.addFeatures( [lbl] );
			var ki =  r.idx;
			if(!idx_dic[ki]){
				idx_dic[ki] = {count: 0, points: []}
			}
			idx_dic[ki].count =  idx_dic[ki].count + 1;
			idx_dic[ki].points.push(r);
		}
	}
	//console.log(idx_dic);
	
	//var lines
	var line_points = [];
	for(var r in idx_dic){
		//console.log(r, idx_dic[r]);
		if(idx_dic[r].count == 1){
			line_points.push(idx_dic[r].points[0]);
		}
	}
	
	var trk_length = line_points.length;
	var points = [];
	//var points;
	var p;
	//console.log(line_points);
	for(var i =0; i < trk_length; i++){
		p = line_points[i];
		points.push(
				new OpenLayers.Geometry.Point(p.lon, p.lat
					).transform(this.get_display_projection(),  this.get_map().getProjectionObject() )
			  );
	}
	var line = new OpenLayers.Geometry.LineString(points);

	var style = { 
		strokeColor: '#0000ff', 
		strokeOpacity: 0.3,
		strokeWidth: 1
	};

	var lineFeature = new OpenLayers.Feature.Vector(line, null, style);
	this.fpLineLayer.addFeatures([lineFeature]);
	this.get_map().zoomToExtent(this.fpLineLayer.getDataExtent()); 
	//this.get_map().zoomOut();
	
	this.fpLabelsLayer.addFeatures( navLabels );
	
},
show_blip: function(obj){
	console.log("L=", this.L);
	this.L.blip.removeAllFeatures();
	var lonLat = new OpenLayers.LonLat(obj.lon, obj.lat
		).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );

	this.get_map().panTo( lonLat );
	this.get_map().zoomTo( 10 );
	
	
	var pt =  new OpenLayers.Geometry.Point(obj.lon, obj.lat
				).transform(this.get_display_projection(), this.get_map().getProjectionObject() );	
	var circle = OpenLayers.Geometry.Polygon.createRegularPolygon(
		pt,
			0, // wtf. .I want a larger cicle
			20
		);
	var style = {
		strokeColor: "red",
		strokeOpacity: 1,
		strokeWidth: 4,
		fillColor: "yellow",
		fillOpacity: 0.8 };
	var feature = new OpenLayers.Feature.Vector(circle, null, style);
	this.L.blip.addFeatures([feature]);
}

});
