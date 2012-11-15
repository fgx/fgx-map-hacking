







//Ext.Ajax.disableCaching = false;







//================================================================
function FGxAirports(){
	
var self = this;

//==========================================================================================
// Airports Store
this.airportsStore = new Ext.data.JsonStore({
	idProperty: "apt_icao",
	fields: [ 	{name: "flag", type: 'int'},
				{name: "is_icao", type: 'bool'},
				{name: "apt_icao", type: 'string'},
				{name: "apt_name", type: 'string'}
	],
	proxy: new Ext.data.HttpProxy({
		url: "/ajax/airports",
		method: 'GET',
		
	}),
	root: "airports",
		remoteSort: false,
	sortInfo: {field: "apt_icao", direction: 'ASC'}
});

this.load_airports = function(){
	self.airportsStore.load({add: true});
};


this.txtSearch = new Ext.form.TextField({
	allowBlank: false,
	emptyText: "<icao>",
	enableKeyEvents: true,
	minLength: 2,
	maxLength: 4
});
this.txtSearch.on("keydown", function(fld, e){
	if( e.getKey() == e.ENTER ){
		var v = fld.getValue();
		console.log(v);
		self.airportsStore.load({params: {apt_icao: v}});
	}
});


this.airportsGrid = new Ext.grid.GridPanel({
	title: 'Airports',
	ssiconCls: 'iconPilots',
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No airports', forceFit: true}, 
	store: this.airportsStore,
	loadMask: false,
	columns: [  //this.selModel,	
		{header: 'Apt ICAO',  dataIndex:'apt_icao', sortable: true},
		{header: 'Apt Name',  dataIndex:'apt_name', sortable: true}
	],
	tbar:[
		this.txtSearch
	],
	
	listeners: {},
	
	bbar: [	//this.pilotsDataCountLabel
		{text: 'Refresh', handler: this.load_airports },
		//{text: 'Send Ws', handler: function(){
		//		self.webSocket.send( "wello" );
		//	}
		//}
	]
});
/*
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
*/





//===================================================================
this.tabPanel  = new Ext.TabPanel({
		sslayout: 'fit',
		activeTab: 0,
		region: 'center',
		width: 600,
		ssplain: true,
		items: [
			this.airportsGrid,
			
		]
	
});


//===================================

new  Ext.Viewport({
	layout: "border",
	ssplain: true,
	items: [
		
		//{region: "north", height: 30	},
		
		//east
		this.tabPanel		
		  // west
		//this.mapPanel,

		
		
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


//this.load_airports();

//============================================================
/*
this.flightsStore.on("add", function(store, recs, idx){
	//console.log(recs);
	Ext.each(recs, function(rec){
		//var rec = recs[i];
		//console.log(rec.get("callsign"));
		// = show_radar (mcallsign, mlat, mlon, mheading, maltitude)
		self.show_radar(rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("altitude"));
	}, this);
});
*/

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