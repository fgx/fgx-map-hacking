
Ext.namespace("FGx");

FGx.NavWidget = Ext.extend(Ext.grid.GridPanel, {


constructor: function(config) {
	
	config = Ext.apply({
		title: 'NavAids',
		iconCls: 'icoFix',
		autoScroll: true,
		autoWidth: true,
		enableHdMenu: false,
		viewConfig: {
			emptyText: 'No items', 
			forceFit: true,
			deferEmptyText: false
		}, 
		store: this.get_store(),
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
				title: "Fix",
				columns: 3,
				items: [
					{iconCls: "icoClr", scope: this,
						handler: function(){
							this.get_fix_search_text().setValue("");
							this.get_fix_search_text().focus();
						}
					},
					this.get_fix_search_text(),
					{text: "Nearby"}
				]
			},
			{xtype: 'buttongroup',
				title: "VOR/DME",
				columns: 3,
				items: [
					{iconCls: "icoClr",	scope: this,
						handler: function(){
							this.get_vor_search_text().setValue("");
							this.get_vor_search_text().focus();
						}
					},
					this.get_fix_search_text(),
					{text: "Nearby"}
				]
			},
			{xtype: 'buttongroup',
				title: "NDB",
				columns: 3,
				items: [
					{iconCls: "icoClr",	scope: this,
						handler: function(){
							this.get_ndb_search_text().setValue("");
							this.get_ndb_search_text().focus();
						}
					},
					this.get_ndb_search_text(),
					{text: "Nearby"}
				]
			}
		],
		listeners: {
			scope: this,
			rowclick:  function(grid, rowIdx, e){
				var rec = this.get_store().getAt(rowIdx);
				//console.log("lat/lon", rec, rec.get("lon"), rec.get("lat"));
				obj = {};
				obj.lat = rec.get("lat");
				obj.lon = rec.get("lon");
				obj.title = rec.get("fix");
				//var lonLat = new OpenLayers.LonLat(rec.get("lon"), rec.get("lat") );
				this.fireEvent("GOTO", obj);
				//self.conf.mapPanel.map.setCenter( new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")) );
			}
		}
		
	}, config);
	
	FGx.NavWidget.superclass.constructor.call(this, config);
}, // Constructor	





		
//== Store
get_store: function(){
	if(!this.xStore){
		this.xStore = new Ext.data.JsonStore({
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
	}
	return this.xStore;
},



//=======================================================
// Search Form
//=======================================================
get_fix_search_text: function(){
	if(!this.txtSearchFix){
		this.txtSearchFix = new Ext.form.TextField({
			width: 50,
			enableKeyEvents: true
		});
		this.txtSearchFix.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_fix_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length == 0){
					return;
				}
				this.get_store().load({params: {q: txt, type: "fix"}});
			}
		}, this);
	}
	return this.txtSearchFix;
},
get_vor_search_text: function(){
	if(!this.txtSearchVor){
		this.txtSearchVor = new Ext.form.TextField({
			width: 50,
			enableKeyEvents: true
		});
		this.txtSearchVor.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_vor_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length == 0){
					return;
				}
				this.get_store().load({params: {q: txt, type: "vor"}});
			}
		}, this);
	}
	return this.txtSearchVor;
},
get_ndb_search_text: function(){
	if(!this.txtSearchNdb){
		this.txtSearchNdb = new Ext.form.TextField({
			width: 50,
			enableKeyEvents: true
		});
		this.txtSearchNdb.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_ndb_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length == 0){
					return;
				}
				this.get_store().load({params: {q: txt, type: "vor"}});
			}
		}, this);
	}
	return this.txtSearchNdb;
},


});
/*
this.txtSearchVorDme = new Ext.form.TextField({
	width: 50,
	enableKeyEvents: true
});
*/







