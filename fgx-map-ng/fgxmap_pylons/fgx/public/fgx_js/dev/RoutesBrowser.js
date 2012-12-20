

//================================================================
Ext.define("FGx.dev.RoutesBrowser",  {

extend: "Ext.Panel",

//======================================================
grid_routes: function(){
	if(!this.gridRoutes){
		this.gridRoutes = Ext.create("Ext.grid.Panel", {
			region: 'center',
			title: "Urls",
			width: 200,
			store:  new Ext.data.JsonStore({
				fields: [	
					{name: "url", type:"string"}
				],
				idProperty: "url",
				
				proxy: {
					type: "ajax",
					url: "/ajax/dev/routes",
					method: 'GET',
					reader: {
						type: "json",
						root: "routes"
					}
				},
				autoLoad: true
			}),
			viewConfig:{
				forceFit: true
			},
			columns: [ 
				{header: "Url", dataIndex: "url", flex:1, menuDisabled: true,
					renderer: function(val, meta, record, idx){
						meta.style = "font-weight: bold;"
						return val;
					}
				}
				//{header: "rows", dataIndex: "rows"}
			],
			listeners:{
				scope: this,
				selectionchange: function(grid, selection, e){
					return
					if(selection.length == 0){
						return;
					}
					var rec = selection[0];
					var table = rec.get("table");
					var url = "/ajax/dev/database/" + this.curr_database + "/table/" + table + "/columns";
					this.grid_columns().getStore().getProxy().url = url;
					this.grid_columns().getStore().load();
				}
			}
		});
	}
	return this.gridRoutes;
},




on_select_db: function(butt, checked){
	if(checked){
		this.curr_database = butt.text;
		
		this.grid_columns().getStore().removeAll();
		
		this.grid_tables().getStore().getProxy().url = "/ajax/dev/database/" + this.curr_database + "/tables";
		this.grid_tables().getStore().load();
	}
	butt.setIconCls( checked ? "icoOn" : "icoOff");
},


initComponent: function() {
	
	Ext.apply(this, {
		layout: 'border',
		fgxType: "DbBrowser",
		title: "DB Schema",
		iconCls: "icoDatabase",
		activeTab: 0,
		tbar: [
			{xtype: 'buttongroup', 
				title: 'Select Database',
				columns: 3,
				items: [
					{text: "navdata", pressed: true, enableToggle: true, toggleGroup: "sel_db", allowDepress: false,
						toggleHandler: this.on_select_db, scope: this, iconCls: "icoOn"},
					{text: "users", enableToggle: true, toggleGroup: "sel_db",  allowDepress: false,
						toggleHandler: this.on_select_db, scope: this, iconCls: "icoOff"},
					{text: "mpnet",  enableToggle: true,  toggleGroup: "sel_db",  allowDepress: false,
						toggleHandler: this.on_select_db, scope: this, iconCls: "icoOff"},
				]
			}
		],
		//height: window.innerHeight - 5,
		items: [
			this.grid_routes(),
			
		]
	
	});
	this.callParent();
	
},

//this.tablesGrid.load_tables();
load:  function(){
	this.grid_tables().getStore().load();
}

});  // end function cinstructor