
Ext.namespace("FGx");

FGx.NavWidget = function(){

var self = this;	
	
//== Store
this.store = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	
		{name: "fix", type: 'string'},
		{name: "lat", type: 'string'},
		{name: "lon", type: 'string'}
	],
	proxy: new Ext.data.HttpProxy({
		url: '/ajax/fix',
		method: "GET"
	}),
	root: 'fix',
	remoteSort: false,
	sortInfo: {
		field: "fix", 
		direction: 'ASC'
	}
});



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
	columns: [ 
		{header: 'Fix', dataIndex:'fix', sortable: true, align: 'left', hidden: false,
			renderer: function(v, meta, rec){
				// @TODO Make this a css class
				return "<b>" + v + "</b>";
			}
		},
		{header: 'Lat', dataIndex:'lat', sortable: true, align: 'left', hidden: false},
		{header: 'Lon', dataIndex:'lon', sortable: true, align: 'left', hidden: false}
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
