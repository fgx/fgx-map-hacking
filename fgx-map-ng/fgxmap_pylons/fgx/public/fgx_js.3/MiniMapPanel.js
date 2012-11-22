
Ext.namespace("FGx");

FGx.MiniMapPanel = Ext.extend(GeoExt.MapPanel, {

L:{},
	
//var self = this;
get_display_projection: function(){
	return new OpenLayers.Projection("EPSG:4326");
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
		this.xMap.events.register("mousemove", this, function (e) {
			
		});
	}
	return this.xMap;
},

	
//var self = this;
get_display_projection: function(){
	return new OpenLayers.Projection("EPSG:4326");
},

//======================================================
// Create the Layers
get_layers: function(){
	this.L.blip = new OpenLayers.Layer.Vector("Blip");
	this.L.line = new OpenLayers.Layer.Vector("Line");
	var arr = [];
	arr.push(this.L.blip);
	arr.push(this.L.line);
	arr.push( 		new OpenLayers.Layer.OSM.Mapnik( "OSM" ) );
	return arr;
},
	
show_blip: function(obj){
	
	this.highLightMarkers.removeAllFeatures();
	var lonLat = new OpenLayers.LonLat(obj.lon, obj.lat
				).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
		
	
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
	
	this.get_map().panTo( lonLat );
},
show_line: function(obj){
	
	this.highLightMarkers.removeAllFeatures();
	var lonLat = new OpenLayers.LonLat(obj.lon, obj.lat
				).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
		
	
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
	
	this.get_map().panTo( lonLat );
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
		
		frame: false, plain: true,border: 0,	bodyBorder: false,
		iconCls: "icoMap",
		hideHeader: true,		
				map: this.get_map(),
				center:  ll, 
				zoom: 2,
				layers: this.get_layers()
		
		
	}, config);
	FGx.MiniMapPanel.superclass.constructor.call(this, config);

	
}, // Constructor	




});


