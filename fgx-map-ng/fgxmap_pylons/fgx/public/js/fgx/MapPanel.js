
Ext.namespace("FGx");
		
FGx.MapPanel = function(){
	
	var xCenterPoint = new OpenLayers.LonLat(939262.20344,5938898.34882);	
	
	var xDisplayProjection = new OpenLayers.Projection("EPSG:4326");
	var xProjection = new OpenLayers.Projection("EPSG:3857");
	
	var xMap = new OpenLayers.Map({
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
	
	FGx.MapPanel.superclass.constructor.call(this, {
		title: "Foo",
		frame: false,
		plain: true,
		border: 0,
		bodyBorder: false,
		region: "center",
			// we do not want all overlays, to try the OverlayLayerContainer
		map: xMap,
		center: xCenterPoint,
		zoom: 5,
		layers: LAYERS,
		
	});
	
	
	
	
} /* end MapPanel */

Ext.extend(FGx.MapPanel,GeoExt.MapPanel, {
	initComponent: function(){
		FGx.MapPanel.superclass.initComponent.apply(this, arguments);
	},
	onRender: function(){
		FGx.MapPanel.superclass.onRender.apply(this, arguments);
	},
});