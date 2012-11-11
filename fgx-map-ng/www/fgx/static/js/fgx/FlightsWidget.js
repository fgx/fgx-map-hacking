
Ext.namespace("FGx");

FGx.FlightsWidget = function(){

var self = this;

this.refresh_rate = 0;

//= Triggered when a refresh toolbar button is clicked
this.on_refresh_toggled = function(butt, checked){
	butt.setIconClass( checked ? "icoOn" : "icoOff");
	if(checked){
		self.refresh_rate = parseInt(butt.ref_rate, 10);
	}
}

//= Riggered for reshresh now
this.on_refresh_now = function(){
	self.store.load();
}

//===========================================================
//== Store
this.store = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	{name: 'flag', type: 'int'},
				{name: 'check', type: 'int'},
				{name: "callsign", type: 'string'},
				{name: "server", type: 'string'},
				{name: "model", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lon", type: 'float'},
				{name: "alt_ft", type: 'int'},
				{name: "spd_kts", type: 'int'},
				//{name: "alt_trend", type: 'string'},
				{name: "heading", type: 'string'}
	],
	url: '/ajax/mp/flights/cf',
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


//===========================================================
//== Renderers 
// @todo: pete to put in css
this.render_callsign = function(v, meta, rec){
	return "<b>" + v + "</b>";
}


//===========================================================
//== Grid
this.grid = new Ext.grid.GridPanel({
	title: 'Live MultiPlayer',
	iconCls: 'icoFlights',
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No flights online', forceFit: true}, 
	store: this.store,
	loadMask: true,
	//sm: new  Ext.grid.RowSelectionModel(),
	columns: [ 
		//{header: 'F',  dataIndex:'flag', sortable: true, width: 40, hidden: false},
		{header: 'CallSign',  dataIndex:'callsign', sortable: true, renderer: this.render_callsign, width: 140},
		{header: 'Aircraft',  dataIndex:'model', sortable: true, sssrenderer: this.render_callsign, hidden: false}, 
		{header: 'Alt', dataIndex:'alt_ft', sortable: true, align: 'right',
			renderer: this.render_altitude
		},
		{header: '', dataIndex:'alt_trend', sortable: true, align: 'center', width: 20,	hidden: true,
			renderer: this.render_altitude_trend},
		{header: 'Hdg', dataIndex:'heading', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v; //Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Dist', dataIndex:'dist', sortable: true, align: 'right', hidden: true,
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v; //Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Spd', dataIndex:'spd_kts', sortable: true, align: 'right', 
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
	
	tbar: [	//this.pilotsDataCountLabel
		{xtype: 'buttongroup',
            title: 'Refresh Secs',
            columns: 7,
            items: [
				{text: "Now", iconCls: "icoRefresh",  handler: this.on_refresh_now},
				{text: "Off", iconCls: "icoOn", pressed: true, enableToggle: true, 
					toggleGroup: "ref_rate", ref_rate: 0, toggleHandler: this.on_refresh_toggled},
				{text: "2", iconCls: "icoOff", enableToggle: true,  
					toggleGroup: "ref_rate", ref_rate: 2, toggleHandler: this.on_refresh_toggled},
				{text: "3", iconCls: "icoOff", enableToggle: true,  
					toggleGroup: "ref_rate", ref_rate: 3, toggleHandler: this.on_refresh_toggled},
				{text: "4", iconCls: "icoOff", enableToggle: true,  
					toggleGroup: "ref_rate", ref_rate: 4, toggleHandler: this.on_refresh_toggled},
				{text: "5", iconCls: "icoOff", enableToggle: true,  
					toggleGroup: "ref_rate", ref_rate: 5, toggleHandler: this.on_refresh_toggled},
				{text: "10", iconCls: "icoOff", enableToggle: true,  
					toggleGroup: "ref_rate", ref_rate: 6, toggleHandler: this.on_refresh_toggled}
            ]   
		}
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
	



} //< FGx.FlightsWidget
