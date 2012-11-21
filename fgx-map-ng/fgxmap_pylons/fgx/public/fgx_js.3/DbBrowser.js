
Ext.namespace("FGx");
//================================================================
FGx.DbBrowser = Ext.extend(Ext.Panel, {
	
//======================================================
// Stores
/*
sssstoreTables:  new Ext.data.JsonStore({
	fields: [	
		{name: "table", type:"string"}
	
	],
	idProperty: "table",
	ssortInfo: {},
	proxy: new Ext.data.HttpProxy({
		url: "/ajax/database/tables",
		method: 'GET'
	}),
	root: "tables"
}),

sssstoreColumns: new Ext.data.JsonStore({
	fields: [	
		{name: "column", type:"string"},
		{name: "type", type:"string"},
		{name: "max_char", type:"string"}
	
	],
	idProperty: "column",
	proxy: new Ext.data.HttpProxy({
		url: "/ajax/database/table/_TABLE_NAME_/columns",
		method: 'GET'
	}),
	root: "columns",
	autoLoad: false
	
}),
*/

//======================================================
// Tables Grid
grid_tables: function(){
	if(!this.gridTables){
		this.gridTables = new Ext.grid.GridPanel({
			region: 'center',
			title: "Tables",
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
				root: "tables"
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
				},
				{header: "rows", dataIndex: "rows"}
			],
			listeners:{
				scope: this,
				rowclick: function(grid, idx, e){
					
					console.log("yes");
					//var r = this
					var rec = self.storeTables.getAt(idx);
					var table = rec.get("table");
					var url = "/ajax/database/table/" + table + "/columns";
					console.log(url);
					self.storeColumns.proxy.setUrl(url);
					self.storeColumns.load();
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
			width: 500,
			store: new Ext.data.JsonStore({
				fields: [	
					{name: "column", type:"string"},
					{name: "type", type:"string"},
					{name: "max_char", type:"string"}
				
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
				{header: "Type", dataIndex: "type"}
			],
			listeners:{
				rowclick: {
					scope: this,
					//##fn: this.on_table_row_click
				}
			}
		});
	}
	return this.gridColumns;
},


/*
this.tablesGrid.on("TABLE", function(table){
	this.columnsGrid.load_columns(table);	
}, this);
*/


constructor: function(config) {
	
	config = Ext.apply({
		layout: 'border',
		renderTo: "widget_div",
		activeTab: 0,
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