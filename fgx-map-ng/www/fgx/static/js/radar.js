







//Ext.Ajax.disableCaching = false;







//================================================================
function FGxRadar(){
	
var self = this;

this.icons = {};

this.icons.level = {}
this.icons.level.blue		= '/static/img/level_blue.png';
this.icons.level.red		= '/static/img/level_red.png';

this.icons.climb = {}
this.icons.climb.blue		= '/static/img/climb_blue.png';
this.icons.climb.red		= '/static/img/climb_red.png';

this.icons.descend = {}
this.icons.descend.blue		= '/static/img/descend_blue.png';
this.icons.descend.red		= '/static/img/descend_red.png';


this.wsLogRecord =  Ext.data.Record.create([
		{name: 'type'},
		{name: 'data'}
]);

//************************************************
//** WebSocket
//************************************************
this.webSocket = 0;
this.create_socket = function (){


	//*** Create Socket
	self.webSocket = new WebSocket(WS_ADDRESS);

	//* On Open Socket
	self.webSocket.onopen = function(evt) { 
		console.log("WS Connects");
	}

	//* On Close Socket
	self.webSocket.onclose = function(evt) { 
		//self.statusLabel.setText("Closed");
		console.log("WS Closed");
		//setTimeout(self.create_socket, 3000); // reattempt login
	}

	//* On Message Resieved Socket
	self.webSocket.onmessage = function(evt) { 
		//console.log("WS Mess", evt.data);
		self.add_ws_log(evt.data);
		
		
	}
	
	self.webSocket.onerror = function(evt) { 
		console.log("WS ERROR", evt);
		
	}
	//alert("ere");
}

this.add_ws_log = function(data_str){
	var js = Ext.decode(data_str)
	var r = new self.wsLogRecord({
		mess_type: js.mess_type, data: data_str	
	});
	self.webSocketStore.insert(0, r);
	console.log("add_log", data_str, js)
	
}

//========================================================================

this.osmprojection = new OpenLayers.Projection("EPSG:4326");

var options = { 

	controls: [
		new OpenLayers.Control.Navigation()
		//new OpenLayers.Control.Measure()
	],
	
	units: 'm',

	// this is the map projection here
	projection: new OpenLayers.Projection("EPSG:900913"),

	//sphericalMercator: true,

	// this is the display projection, I need that to show lon/lat in degrees and not in meters
	displayProjection: new OpenLayers.Projection("EPSG:4326"),

	// the resolutions are calculated by tilecache, when there is no resolution parameter but a bbox in
	// tilecache.cfg it shows you resolutions for all calculated zoomlevels in your browser: 
	// by http://yoururltothemap.org/tilecache.py/1.0.0/layername/ etc.
	// (This would not be necessary for 4326/900913 because this values are widely spread in
	// openlayer/osm/google threads, you will find the resolutions there)
	resolutions: [
		156543.03390624999883584678,
		78271.51695312499941792339,
		39135.75847656249970896170,
		19567.87923828124985448085,
		9783.93961914062492724042,
		4891.96980957031246362021,
		2445.98490478515623181011,
		1222.99245239257811590505,
		611.49622619628905795253,
		305.74811309814452897626,
		152.87405654907226448813,
		76.43702827453613224407,
		38.21851413726806612203,
		19.10925706863403306102,
		9.55462853431701653051,
		4.77731426715850826525,
		2.38865713357925413263,
		1.19432856678962706631,
		0.59716428339481353316,
		0.29858214169740676658
	],

	// I set a max and min resolution, means setting available zoomlevels by default
	maxResolution: 156543.03390624999883584678,
	minResolution: 0.29858214169740676658,

	// i.e. maxExtent for EPSG 3572 is derived by browsing the very useful map at
	// http://nsidc.org/data/atlas/epsg_3572.html. I tried to get this values with mapnik2 and
	// proj4, but the values I get back with box2d are not very useful at the moment
	maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),

	// zoomlevels 0-13 = 14 levels ?
	zoomLevels: 20
};

var extent = new OpenLayers.Bounds(-5, 35, 15, 55);
var centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);




//===================================
this.mapnik_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
this.mapnik_light.setOpacity(0.4);

this.layerR = new OpenLayers.Layer.WMS(
	"Global Imagery",
	"http://maps.opengeo.org/geowebcache/service/wms",
	{layers: "bluemarble"},
	{isBaseLayer: true}
);



this.fgx_ne_landmass = new OpenLayers.Layer.WMS(
	"NE Landmass",
	"http://map.fgx.ch:81/mapnik/fgxcache.py?",
	{
		layers: 'fgx_ne_landmass', 
		format: 'image/png', 
		isBaselayer: true 
	}
);
this.fgx_850_apt = new OpenLayers.Layer.WMS( "850 Airfield", 
	"http://map.fgx.ch:81/mapnik/fgxcache.py?", 
	{
		layers: 'fgx_850_apt', 
		format: 'image/png',
		transparent:'TRUE',
		ssisBaselayer: true 
	},
	{
	visibility:false
	}
);
				
this.fgx_850_vor = new OpenLayers.Layer.WMS( 
	"850 VOR", "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
	{
		layers: 'fgx_850_vor', 
		format: 'image/png',
		transparent:'TRUE'
	},
	{
		visibility:false
	}
);


//==================================================================

//=================================================================
// style for radar Image
this.radarImageMarkerStyle = new OpenLayers.StyleMap({
    "default": {
        strokeColor: "lime",
        strokeWidth: 1,
        fillColor: "lime",

		externalGraphic: "/static/img/radar_blip2.png",
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
});

// style for the marker beside your plane on radar
this.radarLabelMarkerStyle = new OpenLayers.StyleMap({
    
    "default": {
		fill: true,
		fillOpacity: 1,
		fillColor: "black",
        strokeColor: "green",
        strokeWidth: 1,

		//graphic: false,
		externalGraphic: "/static/img/fgx-background-black.png",
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

});



// add Radar vector marker
this.radarImageMarkers = new OpenLayers.Layer.Vector("Radar Markers", {styleMap:  this.radarImageMarkerStyle});


// add Radar label
this.radarLabelMarkers = new OpenLayers.Layer.Vector("Radar Label", {styleMap:  this.radarLabelMarkerStyle});


// create select feature control
this.radarSelectCtrl = new OpenLayers.Control.SelectFeature(this.radarLabelMarkers);
	

//===================================================
this.map = new OpenLayers.Map(options);

this.mapPanel = new GeoExt.MapPanel({

	region: "center",
	DDDid: "mappanel",
	title: "FGx Radar",
	xtype: "gx_mappanel",
	map: this.map,
	layers: [
		this.fgx_ne_landmass,
		//mapnik,
		this.layerR,
		this.mapnik_light,
		this.fgx_850_apt,
		this.fgx_850_vor,
		this.radarImageMarkers,
		this.radarLabelMarkers
	],
	extent: extent,
	center: new OpenLayers.LonLat(939262.20344,5938898.34882),
	zoom: 7,
	split: true,
	items: [
		{xtype: "gx_zoomslider",
			vertical: true,
			height: 300,
			x: 10,
			y: 20,
			plugins: new GeoExt.ZoomSliderTip()
		}
	]
		
});

//=== Layers Tree
this.layerList = new GeoExt.tree.LayerContainer({
	text: 'All Layers',
	layerStore: this.mapPanel.layers,
	leaf: false,
	expanded: true
});
this.layerTree = new Ext.tree.TreePanel({
	title: 'Map Layers',
	region: "west",
	width: 200,
	//renderTo: 'layerTree',
	root: this.layerList
});


//=================================================================================

this.render_callsign = function (v, meta, rec){
	return v
	switch(rec.get('flag')){
		case 0: //* pilot is flying
			meta.css = 'fg_pilot_fly';
			break;
		case 1: //* pilot is new
			meta.css = 'fg_pilot_new';
			break;
		default: //* pilot is < 0 = delete timer
			meta.css = 'fg_pilot_dead';
			break;
	}
	return v;
}


//*****************************************
//** Altirude Related
//*****************************************
this.render_altitude = function (v, meta, rec, rowIdx, colIdx, store){
	return "<span style='color:" + self.altitude_color(v) + ";'>" + Ext.util.Format.number(v, '0,000'); + '</span>';
}
this.render_altitude_trend = function (v, meta, rec, rowIdx, colIdx, store){
	return "<img src='" + self.altitude_image(v, rec.get('check') == 1) + "'>";
}
this.altitude_image = function(alt_trend, is_selected){
	var color = is_selected ? 'red' : 'blue';
	if(alt_trend == 'level'){
		return self.icons.level[color];
	}
	//return "Foo"
	return alt_trend == 'climb' ? self.icons.climb[color] : self.icons.descend[color];
}
this.altitude_color = function(v){
	if(v < 1000){
		color = 'red';
	}else if(v < 2000){
		color = '#FA405F';
	}else if(v < 4000){
		color = '#A47F24';
	}else if(v < 6000){
		color = '#7FFA40';
	}else if(v < 8000){
		color = '#40FA6E';
	}else if(v < 10000){
		color = '#40FAAA';
	}else if(v < 15000){
		color = '#FA405F';
	}else if(v < 20000){
		color = '#40FAFA';
	}else{
		color = '#331CDC';
	}
	return color;

}

//==========================================================================================
// Store
this.flightsStore = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	{name: 'flag', type: 'int'},
				{name: 'check', type: 'int'},
				{name: "callsign", type: 'string'},
				{name: "mpserver", type: 'string'},
				{name: "aero", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lon", type: 'float'},
				{name: "altitude", type: 'int'},
				{name: "alt_trend", type: 'string'},
				{name: "heading", type: 'string'},
				{name: "dist", type: 'string'}
	],
	url: '/ajax/flights',
	root: 'flights',
	remoteSort: false,
	sortInfo: {field: "callsign", direction: 'ASC'}
});

this.load_flights = function(){
	self.flightsStore.load({add: true});
};


this.flightsGrid = new Ext.grid.GridPanel({
	title: 'Flights Data',
	ssiconCls: 'iconPilots',
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No flights online', forceFit: true}, 
	store: this.flightsStore,
	loadMask: false,
	columns: [  //this.selModel,	
		{header: 'F',  dataIndex:'flag', sortable: true, width: 40, hidden: true},
		{header: 'CallSign',  dataIndex:'callsign', sortable: true, renderer: this.render_callsign, width: 100},
		{header: 'Aircraft',  dataIndex:'aero', sortable: true, sssrenderer: this.render_callsign, hidden: true}, 
		{header: 'Alt', dataIndex:'altitude', sortable: true, align: 'right',
			renderer: this.render_altitude
		},
		{header: '', dataIndex:'alt_trend', sortable: true, align: 'center', width: 20,	hidden: true,
			renderer: this.render_altitude_trend},
		{header: 'Heading', dataIndex:'heading', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v; //Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Dist', dataIndex:'dist', sortable: true, align: 'right', hidden: true,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v; //Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Airspeed', dataIndex:'airspeed', sortable: true, align: 'right', hidden: true,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Lat', dataIndex:'lat', sortable: true, align: 'right', hidden: false,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0.00000');
			}
		},
		{header: 'Lon', dataIndex:'lon', sortable: true, align: 'right', hidden: false,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0.00000');
			}
		},
		{header: 'Server', dataIndex:'server', sortable: true, align: 'left', hidden: true,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v;
			}
		}

	],
	listeners: {},
	
	bbar: [	//this.pilotsDataCountLabel
		{text: 'Refresh', handler: this.load_flights },
		//{text: 'Send Ws', handler: function(){
		//		self.webSocket.send( "wello" );
		//	}
		//}
	]
});
this.flightsGrid.on("rowdblclick", function(grid, idx, e){
	var callsign = self.flightsStore.getAt(idx).get("callsign");
	//console.log(">>>>>>>>", callsign);
	var existing_img = self.radarImageMarkers.getFeatureBy("_callsign", callsign);
	//console.log("exist=", existing_img);
	if(existing_img){
		//radarImageMarkers.removeFeatures(existing_img);
		//console.log("geom=", existing_img.geometry);
	
		self.map.setCenter(
			existing_img.geometry.transform(
				self.osmprojection,
				self.map.getProjectionObject()
			)
		);
	}
	//var latlng = new google.maps.LatLng(rec.get('lat'), rec.get('lng'));
	//self.Map.panTo(latlng);
});  

//==========================================================================================
// Mp Servers Store
this.mpServersStore = new Ext.data.JsonStore({
	idProperty: 'host',
	fields: [ 	{name: 'flag', type: 'int'},
				
				{name: "host", type: 'string'},
				{name: "ip", type: 'string'},
				{name: "flights_connected", type: 'string'},
				{name: "flights_total", type: 'int'},
				{name: "flights_connected", type: 'int'},
				{name: "lag", type: 'int'},
				{name: "status", type: 'string'},
				{name: "last_polled", type: 'date'},
				{name: "last_seen", type: 'date'},
	],
	url: '/ajax/mpservers',
	root: 'mpservers',
	remoteSort: false,
	sortInfo: {field: "host", direction: 'ASC'}
});
this.load_mpservers = function(){
	self.mpServersStore.load({add: true});
};

this.render_host = function(v){
	var p = v.split(".");
	return p[0];
}

this.render_last_date = function(v, meta, rec, rowIdx, colIdx, store){
	if(!v){
		return "";
	}
	return v.format("Y-m-d H:i:s");
}

this.mpServersGrid = new Ext.grid.GridPanel({
	title: 'MP Servers',
	ssiconCls: 'iconPilots',
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No servers online', forceFit: true}, 
	store: this.mpServersStore,
	loadMask: false,
	columns: [  //this.selModel,	
		{header: 'F',  dataIndex:'flag', sortable: true, width: 40, hidden: true},
		{header: 'Host',  dataIndex:'host', sortable: true, width: 60, renderer: this.render_host},
		{header: 'Ip',  dataIndex:'ip', sortable: true }, 
		{header: 'Lag', dataIndex:'lag', sortable: true, align: 'right', width: 40
			
		},
		{header: '', dataIndex:'status', sortable: true, align: 'center', width: 20,	hidden: true,
			renderer: this.render_altitude_trend},
		{header: 'Last Seen', dataIndex:'last_seen', sortable: true, align: 'right',width: 50,
			renderer: this.render_last_date
		},
		{header: 'Ckecked', dataIndex:'last_polled', sortable: true, align: 'right', width: 50,
			 renderer: this.render_last_date
		},
		{header: 'Connected', dataIndex:'flights_connected', sortable: true, align: 'right', hidden: false,width: 50,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0');
			}
		}

	],
	listeners: {},
	
	bbar: [	//this.pilotsDataCountLabel
		{text: 'Refresh', handler: this.load_mpservers }
	]
});

//=====================================================================================


//==========================================================================================
// Store
this.webSocketStore = new Ext.data.Store({
	idProperty: 'ts',
	fields: [ 	
				{name: 'dated', type: 'dated'},
				{name: "ts", type: 'string'},
				{name: "data", type: 'string'},
				{name: "mess_type", type: 'string'},
	],
	//url: '/ajax/flights',
	//root: 'flights',
	//remoteSort: false,
	sortInfo: {field: "dated", direction: 'DESC'}
});

this.txtWebSocketMessage = new Ext.form.TextField({
	
});



this.webSocketGrid = new Ext.grid.GridPanel({
	title: 'Web Socket Data',
	ssiconCls: 'iconPilots',
	region: 'south',
	height: 200,
	collaapsible: true,
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No items online', forceFit: true}, 
	store: this.webSocketStore,
	loadMask: false,
	columns: [  //this.selModel,	
		{header: 'TS',  dataIndex:'dated', sortable: true, width: 100},
		{header: 'Type',  dataIndex:'mess_type', sortable: true, width: 100},
		{header: 'Data',  dataIndex:'data', sortable: true}

	],
	
	
	bbar: [	//this.pilotsDataCountLabel
		{text: 'Connect', handler: this.create_socket },
		this.txtWebSocketMessage,
		{text: 'Send Message', 
			handler: function(){
				var m = {	mess_type: "chat", 
							data: {
								message: self.txtWebSocketMessage.getValue()
							} 
				}
				var s = Ext.encode(m)
				self.webSocket.send( s );
			}
		}
	]
});

//===================================================================
this.tabPanel  = new Ext.TabPanel({
		sslayout: 'fit',
		activeTab: 0,
		region: 'east',
		width: 600,
		ssplain: true,
		items: [
			this.flightsGrid, 
			this.layerTree,
			this.mpServersGrid 
			
		]
	
});


//===================================

new  Ext.Viewport({
	layout: "border",
	ssplain: true,
	items: [
		
		//{region: "north", height: 30	},
		
		//east
		this.tabPanel,		
		  // west
		this.mapPanel,
		this.webSocketGrid
		
		
		/*,
		{
			region: "east",
			title: "Description",
			contentEl: "description",
			width: 200,
			split: true
		}
		*/
	]
});

//mapPanel = Ext.getCmp("mappanel");



//==========================================================
// Shows aircraft on the RADAR map, with callsign (two features, poor openlayer)
this.show_radar = function (mcallsign, mlat, mlon, mheading, maltitude){

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

	var pointImg = new OpenLayers.Geometry.Point(mlon, mlat).transform(self.osmprojection, self.map.getProjectionObject() );	
	if(!self.map.getExtent().containsPixel(pointImg, false)){
		return; //alert(map.getExtent().containsLonLat(pointImg, false));
	}

	// Add Image
	var imgFeat = new OpenLayers.Feature.Vector(pointImg, {
				planerotation: mheading
				}); 
	imgFeat._callsign = mcallsign;
	self.radarImageMarkers.addFeatures([imgFeat]);	
	
	
	
	var gxOff = 4;
	var gyOff = -8;

	var lxOff = 6;
	var lyOff = 2;
	
	//+ WTF they are different points +- !!!
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
	var pointLabel = new OpenLayers.Geometry.Point(mlon, mlat).transform(self.osmprojection, self.map.getProjectionObject() );
	var lblFeat = new OpenLayers.Feature.Vector(pointLabel, {
                callsign: mcallsign,
				lxOff: lxOff, lyOff: lyOff,
				gxOff: gxOff, gyOff: gyOff
				});
	lblFeat._callsign = mcallsign;
	self.radarLabelMarkers.addFeatures([lblFeat]);	
	
} // add radar

//============================================================
this.flightsStore.on("add", function(store, recs, idx){
	//console.log(recs);
	Ext.each(recs, function(rec){
		//var rec = recs[i];
		//console.log(rec.get("callsign"));
		// = show_radar (mcallsign, mlat, mlon, mheading, maltitude)
		self.show_radar(rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("altitude"));
	}, this);
});


// equivalent using TaskMgr
/*
Ext.TaskMgr.start({
    run: this.load_flights,
    interval: 8000
});
*/

// equivalent using TaskMgr
/*
Ext.TaskMgr.start({
    run: this.load_mpservers,
    interval: 60000
});
*/
//this.create_socket();


} // end function cinstructor