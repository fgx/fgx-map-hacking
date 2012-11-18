

//================================================================
FGx.DbBrowser = function (){
	
var self = this;

//======================================================
// Stores
this.storeTables = new Ext.data.JsonStore({
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
});
this.storeColumns = new Ext.data.JsonStore({
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
	
});


//======================================================
// Tables Grid
this.gridTables = new Ext.grid.GridPanel({
	region: 'center',
	title: "Tables",
	store: this.storeTables,
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

//=================================================================
//== Columns



this.gridColumns = new Ext.grid.GridPanel({
	region: 'east', 
	title: "Columns",
	width: 500,
	store: this.storeColumns,
	viewConfig:{
		forceFit: true,
		emptyText: "< Select a table",
		deferEmptyText: false
	},
	columns: [ 
		{header: "Column", dataIndex: "column"},
		{header: "Type", dataIndex: "type"}
	],
	listeners:{
		rowclick: {
			scope: this,
			//##fn: this.on_table_row_click
		}
	}
});


/*
this.tablesGrid.on("TABLE", function(table){
	this.columnsGrid.load_columns(table);	
}, this);
*/


//===================================================================
this.tabPanel  = new Ext.Panel({
	layout: 'border',
	renderTo: "widget_div",
	activeTab: 0,
	plain: true,
	height: window.innerHeight - 5,
	items: [
		//this.databasesGrid,
		this.gridTables,
		this.gridColumns
	]
	
});

//this.tablesGrid.load_tables();
this.load = function(){
	this.storeTables.load();
}

} // end function cinstructor