

Ext.define("FGx.nav.NavWidget", {

extend: "Ext.grid.GridPanel",
tbw: 50,

initComponent: function() {
	
	Ext.apply(this, {
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
		
		columns: [ 
			{header: '&nbsp;', dataIndex:'nav_type', width: 20,
				renderer: function(v, meta, rec){
					//meta.attr = 'style= "background-image: url(/images/vfr_fix.png) !important; background-repeat: no-repeat;"';
					
					if(v == "FIX"){
						meta.css = "icoFix";
						
					}else if(v == "NDB"){
						meta.css = "icoNdb";
							
					}else if(v == "VOR"){
						meta.css = "icoVor";
					}
					return " ";
					//return "<img src='/images/vfr_fix.png'>";
				}
			},
			{header: 'Ident', dataIndex:'ident', sortable: true, align: 'left', hidden: false,
				renderer: function(v, meta, rec){
					// @TODO Make this a css class
					return "<b>" + v + "</b>";
				}
			},
			{header: 'Name', dataIndex:'nav_name', sortable: true, align: 'left', hidden: false},
			{header: 'Freq', dataIndex:'nav_freq_khz', sortable: true, align: 'left', hidden: false}
			//{header: 'Lat', dataIndex:'lat', sortable: true, align: 'left', hidden: false},
			//{header: 'Lon', dataIndex:'lon', sortable: true, align: 'left', hidden: false}
		],
		
		/* Top Toolbar */
		tbar: [
			{xtype: 'buttongroup',
				title: "Fix",
				columns: 3,
				items: [
					{iconCls: "icoClr", scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_fix_search_text().setValue("");
							this.get_fix_search_text().focus();
						}
					},
					this.get_fix_search_text()
					//{text: "Nearby"}
				]
			},
			{xtype: 'buttongroup',
				title: "VOR/DME",
				columns: 3,
				items: [
					{iconCls: "icoClr",	scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_vor_search_text().setValue("");
							this.get_vor_search_text().focus();
						}
					},
					this.get_vor_search_text()
					//{text: "Nearby"}
				]
			},
			{xtype: 'buttongroup',
				title: "NDB",
				columns: 3,
				items: [
					{iconCls: "icoClr",	scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_ndb_search_text().setValue("");
							this.get_ndb_search_text().focus();
						}
					},
					this.get_ndb_search_text()
				]
			},
			{xtype: 'buttongroup',
				title: "All",
				columns: 3,
				items: [
					{iconCls: "icoClr",	scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_all_search_text().setValue("");
							this.get_all_search_text().focus();
						}
					},
					this.get_all_search_text()
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
				obj.title = rec.get("ident");
				//var lonLat = new OpenLayers.LonLat(rec.get("lon"), rec.get("lat") );
				this.fireEvent("GOTO", obj);
				//self.conf.mapPanel.map.setCenter( new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")) );
			}
		}
		
	});
	this.callParent();
}, // Constructor	





		
//== Store
get_store: function(){
	if(!this.xStore){
		this.xStore = new Ext.data.JsonStore({
			idProperty: 'callsign',
			fields: [ 	
				{name: "nav_type", type: 'string'},
				{name: "ident", type: 'string'},
				{name: "name", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lon", type: 'float'},
				{name: "freq", type: 'string'}
			],
			proxy: new Ext.data.HttpProxy({
				url: '/ajax/navaids',
				method: "GET"
			}),
			root: 'navaids',
			remoteSort: false,
			sortInfo: {
				field: "ident", 
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
			width: this.tbw,
			enableKeyEvents: true
		});
		this.txtSearchFix.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_fix_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length < 2){
					return;
				}
				this.get_store().load({params: {search: txt, nav_type: "fix"}});
			}
		}, this);
	}
	return this.txtSearchFix;
},
get_vor_search_text: function(){
	if(!this.txtSearchVor){
		this.txtSearchVor = new Ext.form.TextField({
			width: this.tbw,
			enableKeyEvents: true
		});
		this.txtSearchVor.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_vor_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length < 2){
					return;
				}
				this.get_store().load({params: {search: txt, nav_type: "vor"}});
			}
		}, this);
	}
	return this.txtSearchVor;
},
get_ndb_search_text: function(){
	if(!this.txtSearchNdb){
		this.txtSearchNdb = new Ext.form.TextField({
			width: this.tbw,
			enableKeyEvents: true
		});
		this.txtSearchNdb.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_ndb_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length < 2){
					return;
				}
				this.get_store().load({params: {search: txt, nav_type: "ndb"}});
			}
		}, this);
	}
	return this.txtSearchNdb;
},

get_all_search_text: function(){
	if(!this.txtSearchAll){
		this.txtSearchAll = new Ext.form.TextField({
			width: this.tbw,
			enableKeyEvents: true
		});
		this.txtSearchAll.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_all_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length < 2){
					return;
				}
				this.get_store().load({params: {search: txt, nav_type: ""}});
			}
		}, this);
	}
	return this.txtSearchAll;
}


});








