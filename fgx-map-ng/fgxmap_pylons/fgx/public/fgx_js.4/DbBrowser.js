
Ext.namespace("FGx");
//================================================================
FGx.DbBrowser = Ext.extend(Ext.Panel, {

curr_database : "data",

//======================================================
// Tables Grid
grid_tables: function(){
	if(!this.gridTables){
		this.gridTables = new Ext.grid.GridPanel({
			region: 'center',
			title: "Tables",
			width: 200,
			store:  new Ext.data.JsonStore({
				fields: [	
					{name: "table", type:"string"}
				],
				idProperty: "table",
				ssortInfo: {},
				proxy: new Ext.data.HttpProxy({
					url: "/ajax/database/data/tables",
					method: 'GET'
				}),
				root: "tables",
				autoLoad: true
			}),
			viewConfig:{
				forceFit: true
			},
			columns: [ 
				{header: "Table", dataIndex: "table",
					renderer: function(val, meta, record, idx){
						meta.style = "font-weight: bold;"
						return val;
					}
				}
				//{header: "rows", dataIndex: "rows"}
			],
			listeners:{
				scope: this,
				rowclick: function(grid, idx, e){
					
					var rec = this.grid_tables().getStore().getAt(idx);
					var table = rec.get("table");
					var url = "/ajax/database/" + this.curr_database + "/table/" + table + "/columns";
					this.grid_columns().getStore().proxy.setUrl(url);
					this.grid_columns().getStore().load();
				}
			}
		});
	}
	return this.gridTables;
},


//=================================================================
//== Columns
grid_columns: function(){
	if(!this.gridColumns){
		this.gridColumns = new Ext.grid.GridPanel({
			region: 'east', 
			title: "Columns",
			width: "70%",
			store: new Ext.data.JsonStore({
				fields: [	
					{name: "column", type:"string"},
					{name: "type", type:"string"},
					{name: "max_char", type:"string"},
					{name: "nullable", type:"boolean"},
				
				],
				idProperty: "column",
				proxy: new Ext.data.HttpProxy({
					url: "/ajax/database/table/_TABLE_NAME_/columns",
					method: 'GET'
				}),
				root: "columns",
				autoLoad: false
				
			}),
			viewConfig:{
				forceFit: true,
				emptyText: "< Select a table",
				deferEmptyText: false
			},
			columns: [ 
				{header: "Column", dataIndex: "column",
					renderer: function(val, meta, record, idx){
						meta.style = "font-weight: bold;"
						return val;
					}
				},
				{header: "Type", dataIndex: "type"},
				{header: "Nullable", dataIndex: "nullable", width: 30,
					renderer: function(v){
						return v ? "Yes" : "-";
					}
				}
			]
		});
	}
	return this.gridColumns;
},


on_select_db: function(butt, checked){
	if(checked){
		this.curr_database = butt.text;
		
		this.grid_columns().getStore().removeAll();
		
		this.grid_tables().getStore().proxy.setUrl("/ajax/database/" + this.curr_database + "/tables");
		this.grid_tables().getStore().load();
	}
	butt.setIconClass( checked ? "icoOn" : "icoOff");
},


constructor: function(config) {
	
	config = Ext.apply({
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
					{text: "data", pressed: true, enableToggle: true, toggleGroup: "sel_db", 
						toggleHandler: this.on_select_db, scope: this, iconCls: "icoOn"},
					{text: "secure", enableToggle: true, toggleGroup: "sel_db", 
						toggleHandler: this.on_select_db, scope: this, iconCls: "icoOff"},
					{text: "mpnet",  enableToggle: true,  toggleGroup: "sel_db", 
						toggleHandler: this.on_select_db, scope: this, iconCls: "icoOff"},
				]
			}
		],
		plain: true,
		height: window.innerHeight - 5,
		items: [
			this.grid_tables(),
			this.grid_columns()
		]
	
	}, config);
	FGx.DbBrowser.superclass.constructor.call(this, config);
	
},

//this.tablesGrid.load_tables();
load:  function(){
	this.grid_tables().getStore().load();
}

});  // end function cinstructor