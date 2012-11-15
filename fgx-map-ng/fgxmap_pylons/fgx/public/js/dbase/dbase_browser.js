







//Ext.Ajax.disableCaching = false;







//================================================================
FGx.DBaseBrowser = function (){
	
var self = this;

this.database = "";
this.table = ""


//this.databasesGrid = new FGx.DBaseDatabasesGrid({region: 'west', width: 200});
this.tablesGrid = new FGx.DBaseTablesGrid({region: 'center'});
this.columnsGrid = new FGx.DBaseColumnsGrid({region: 'east', width: 300});

/*
this.databasesGrid.on("database", function(database){
	self.database = database;
	self.tablesGrid.load_tables(self.database);	
})
*/;


//===================================================================
this.tabPanel  = new Ext.Panel({
	layout: 'border',
	renderTo: "widget_div",
	activeTab: 0,
	plain: true,
	height: window.innerHeight - 5,
	items: [
		//this.databasesGrid,
		this.tablesGrid,
		this.columnsGrid
	]
	
});

this.tablesGrid.on("table", function(table){
	self.columnsGrid.load_columns(self.database, table);	
});


} // end function cinstructor