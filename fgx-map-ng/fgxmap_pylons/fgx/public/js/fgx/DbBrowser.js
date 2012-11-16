

//================================================================
FGx.DbBrowser = function (){
	

//======================================================
// Tables
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
		rowclick: function(){
			
			console.log("yes");
			//var r = this
		}
	}
});

//=================================================================
//== Columns

this.storeColumns = new Ext.data.JsonStore({
	fields: [	
		{name: "column", type:"string"},
		{name: "type", type:"string"},
		{name: "max_char", type:"string"}
	
	],
	idProperty: "column",
	ssortInfo: {},
	//url: "/ajax/dbase",
	root: "columns",
	autoLoad: false
	
});

this.gridColumns = new Ext.grid.GridPanel({
	region: 'east', 
	title: "Columns",
	width: 300,
	store: this.storeTables,
	viewConfig:{
		forceFit: true
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