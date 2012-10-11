// (c) 2011 Yves Sablonier, Zurich, GPLv2
// based on OpenLayers/mobile/jquery examples

// initialize map when page ready
var map;
var gg = new OpenLayers.Projection("EPSG:4326");
var sm = new OpenLayers.Projection("EPSG:900913");

//var mapnik = new OpenLayers.Layer.OSM.Mapnik( "OSM normal" );
//mapnik.setOpacity(1.0);

//var mapnik_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
//mapnik_light.setOpacity(0.4);

var graticuleLine = new OpenLayers.Symbolizer.Line({
												   strokeColor: "#999999",
												   strokeDashstyle: "longdash",
												   strokeWidth: 0.3
												   });


var graticule = new OpenLayers.Control.Graticule({
												 numPoints: 2, 
												 labelled: true,
												 //autoActivate: false,
												 layerName: "Graticule",
												 labelFormat: "dmm",
												 lineSymbolizer: graticuleLine
												 });



var fgx_ne_landmass = new OpenLayers.Layer.WMS( "NE Landmass", 
											   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
											   {
											   layers: 'fgx_ne_landmass', 
											   format: 'image/png', 
											   isBaselayer: true 
											   }
											   );


var fgx_850_apt = new OpenLayers.Layer.WMS( "850 Airfield", 
										   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
										   {layers: 'fgx_850_apt', 
										   format: 'image/png',
										   transparent:'TRUE'
										   },
										   {
										   visibility:true
										   }
										   );

var fgx_850_vor = new OpenLayers.Layer.WMS( "850 VOR", 
										   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
										   {layers: 'fgx_850_vor', 
										   format: 'image/png',
										   transparent:'TRUE'
										   },
										   {
										   visibility:false
										   }
										   );

var fgx_850_dme = new OpenLayers.Layer.WMS( "850 DME", 
										   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
										   {layers: 'fgx_850_dme', 
										   format: 'image/png',
										   transparent:'TRUE'
										   },
										   {
										   visibility:false
										   }
										   );

var fgx_850_ndb = new OpenLayers.Layer.WMS( "850 NDB", 
										   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
										   {layers: 'fgx_850_ndb', 
										   format: 'image/png',
										   transparent:'TRUE'
										   },
										   {
										   visibility:false
										   }
										   );

var fgx_850_ils = new OpenLayers.Layer.WMS( "850 ILS LOC", 
										   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
										   {layers: 'fgx_850_ils', 
										   format: 'image/png',
										   transparent:'TRUE'
										   },
										   {
										   visibility:false
										   }
										   );

var fgx_850_ils_info = new OpenLayers.Layer.WMS( "850 ILS INFO", 
												"http://map.fgx.ch:81/mapnik/fgxcache.py?", 
												{layers: 'fgx_850_ils_info', 
												format: 'image/png',
												transparent:'TRUE'
												},
												{
												visibility:false
												}
												);

var fgx_850_ils_marker = new OpenLayers.Layer.WMS( "850 ILS OM/MM", 
												  "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
												  {layers: 'fgx_850_ils_marker', 
												  format: 'image/png',
												  transparent:'TRUE'
												  },
												  {
												  visibility:false
												  }
												  );

var fgx_850_fix = new OpenLayers.Layer.WMS( "850 FIX", 
										   "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
										   {layers: 'fgx_850_fix', 
										   format: 'image/png',
										   transparent:'TRUE'
										   },
										   {
										   visibility:false
										   }
										   );


var init = function (onSelectFeatureFunction) {
	var mapnik = new OpenLayers.Layer.OSM.Mapnik( "OSM normal" );
	mapnik.setOpacity(1.0);
	
	var mapnik_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
	mapnik_light.setOpacity(0.4);


    // create map
    map = new OpenLayers.Map({
        div: "map",
        theme: null,
        projection: sm,
        units: "m",
        numZoomLevels: 18,
        maxResolution: 156543.0339,
        maxExtent: new OpenLayers.Bounds(
            -20037508.34, -20037508.34, 20037508.34, 20037508.34
        ),
        controls: [
            new OpenLayers.Control.Attribution(),
            new OpenLayers.Control.TouchNavigation({
                dragPanOptions: {
                    enableKinetic: true
                }
            }),
			graticule
        ],
							 
		layers: [
				 mapnik_light,
				 mapnik,
				 fgx_ne_landmass,
				 fgx_850_apt,
				 fgx_850_vor,
				 fgx_850_dme,
				 fgx_850_ndb,
				 fgx_850_ils,
				 fgx_850_ils_info,
				 fgx_850_ils_marker,
				 fgx_850_fix
        ],
							 
		center: new OpenLayers.LonLat(939262.20344,5938898.34882),
		zoom: 5
    });

};