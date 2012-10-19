
Ext.namespace("FGx");

FGx.NavWidget = function(){

var self = this;	
	
//== Flights Store
this.store = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	{name: "fix", type: 'string'},
				{name: "lat", type: 'string'},
				{name: "lon", type: 'string'}
	],
	url: '/ajax/fix',
	root: 'flights',
	method: "GET",
	remoteSort: false,
	sortInfo: {
		field: "fix", 
		direction: 'ASC'
	}
});

this.load_flights = function(){
	self.store.load();
}

this.txtSearch = new Ext.form.TextField({
	width: 100,
	enableKeyEvents: true
	
});
this.txtSearch.on("keypress", function(txtFld, e){
	console.log("press", e);
	if( e.getKey() == e.ENTER ){
		self.txtSearch.setValue( self.txtSearch.getValue().trim() );
		var txt = self.txtSearch.getValue();
		if(txt.length == 0){
			return;
		}
		self.store.load({params: {search: txt}});
	}
});

//== Grid
this.grid = new Ext.grid.GridPanel({
	title: 'Fix',
	iconCls: 'icoFlights',
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
	
	/* Top Toolbar */
	tbar: [
		{text: "Search Fix", 
			handler: function(){
				self.txtSearch.setValue("");
				self.txtSearch.setFocus();
			}
		},
		this.txtSearch
	]
});

	



} //< FGx.NavWidget
