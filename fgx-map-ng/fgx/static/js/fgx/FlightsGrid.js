
Ext.namespace("FGx");

FGx.FlightsGrid = function(){

var self = this;	
	
//== Flights Store
this.store = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	{name: 'flag', type: 'int'},
				{name: 'check', type: 'int'},
				{name: "callsign", type: 'string'},
				{name: "mpserver", type: 'string'},
				{name: "aero", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lon", type: 'float'},
				{name: "altitude_ft", type: 'int'},
				{name: "alt_trend", type: 'string'},
				{name: "heading", type: 'string'}
	],
	url: '/ajax/mp/flights',
	root: 'flights',
	remoteSort: false,
	sortInfo: {
		field: "callsign", 
		direction: 'ASC'
	}
});

this.load_flights = function(){
	self.store.load();
}

//== Grid
this.grid = new Ext.grid.GridPanel({
	title: 'Flights Data',
	iconCls: 'iconPilots',
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No flights online', forceFit: true}, 
	store: this.store,
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
		{xtype: "checkbox", text: "Auto Refresh"},
		{xtype: "button", text: 'Refresh', handler: this.load_flights,  iconCls: "icoRefresh"}
		
	]
});
this.grid.on("rowdblclick", function(grid, idx, e){
	var callsign = self.flightsStore.getAt(idx).get("callsign");
	console.log(">>>>>>>>", callsign);
	var existing_img = self.radarImageMarkers.getFeatureBy("_callsign", callsign);
	console.log("exist=", existing_img);
	if(existing_img){
		//radarImageMarkers.removeFeatures(existing_img);
		console.log("geom=", existing_img.geometry);
	
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
	



} //< FGx.FlightsGrid
