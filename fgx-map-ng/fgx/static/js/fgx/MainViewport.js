
Ext.namespace("FGx");

FGx.MainViewport = function(){

this.centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);	
	
//============================================================
this.flightsGrid = new FGx.FlightsGrid();




this.mapLayersTree = new FGx.MapLayersTree();


//============================================================
this.mapPanel = new GeoExt.MapPanel({
	border: true,
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
    zoom: 5,
    layers: [

		new OpenLayers.Layer.WMS( "Natural Earth", 
			"http://map.fgx.ch:81/mapnik/fgxcache.py?", {
			layers: 'fgx_ne_landmass', 
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
					"fgx_850_vor",
					"fgx_850_dme",
					"fgx_850_ndb"
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
					"fgx_850_ils",
					"fgx_850_ils_info",
					"fgx_850_ils_marker"
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
		)
				
	]
}); //< mapPanel

//============================================================
// Viewport auto rendered to body
//============================================================
this.viewport = new Ext.Viewport({
	layout: "border",
	plain: true,
	items: [

		this.mapPanel,
		{region: 'east', width: 300, 
			title: "FGx Map - Next Gen",
			xtype: 'tabpanel',
			plain: true,
			border: 0,
			collapsible: true,
			activeItem: 0,
			items: [
				this.flightsGrid.grid,
				this.mapLayersTree.tree
			]
        
		},
	]
});



this.flightsGrid.store.on("add", function(store, recs, idx){
	console.log(recs);
	Ext.each(recs, function(rec){
		//var rec = recs[i];
		console.log(rec.get("callsign"));
		// = show_radar (mcallsign, mlat, mlon, mheading, maltitude)
		//self.show_radar(rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("altitude"));
	}, this);
});
	
	
} //< FGx.MainViewport
