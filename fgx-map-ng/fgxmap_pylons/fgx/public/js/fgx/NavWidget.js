
Ext.namespace("FGx");

FGx.NavWidget = function(conf){

var self = this;	

this.conf = conf;
	
//== Store
this.store = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	
		{name: "fix", type: 'string'},
		{name: "lat", type: 'float'},
		{name: "lon", type: 'float'}
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


//=======================================================
// Search Form
//=======================================================
this.txtSearchFix = new Ext.form.TextField({
	width: 50,
	enableKeyEvents: true
});
this.txtSearchFix.on("keypress", function(txtFld, e){
	console.log("press", e);
	if( e.getKey() == e.ENTER ){
		self.txtSearchFix.setValue( self.txtSearchFix.getValue().trim() );
		var txt = self.txtSearchFix.getValue();
		if(txt.length == 0){
			return;
		}
		self.store.load({params: {search: txt}});
	}
});

this.txtSearchVorDme = new Ext.form.TextField({
	width: 50,
	enableKeyEvents: true
});

//== Grid
this.grid = new Ext.grid.GridPanel({
	title: 'Fix',
	iconCls: 'icoFix',
	autoScroll: true,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No flights online', forceFit: true}, 
	store: this.store,
	loadMask: true,
	sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
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
		{xtype: 'buttongroup',
            title: "find Fix",
            columns: 3,
            items: [
				{text: "Clr",
					handler: function(){
						self.txtSearchFix.setValue("");
						self.txtSearchFix.focus();
					}
				},
				this.txtSearchFix,
				{text: "Neraby"}
			]
		},
		{xtype: 'buttongroup',
            title: "find Vor/Dme",
            columns: 3,
            items: [
				{text: "Clr",
					handler: function(){
						self.txtSearchVorDme.setValue("");
						self.txtSearchVorDme.focus();
					}
				},
				this.txtSearchVorDme,
				{text: "Neraby"}
			]
		}
	]
});
this.grid.on("rowclick", function(grid, rowIdx, e){
	var rec = self.store.getAt(rowIdx);
	console.log("lat/lon", rec, rec.get("lon"), rec.get("lat"));
	self.conf.mapPanel.map.setCenter( new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")) );
});
	



} //< FGx.NavWidget


