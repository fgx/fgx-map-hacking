
FGx.DBaseTablesGrid = Ext.extend(Ext.grid.GridPanel, {
	
    constructor: function(config) {
		
		
		this.storeX = new Ext.data.JsonStore({
			fields: [	
				{name: "table", type:"string"}
			
			],
			idProperty: "table",
			ssortInfo: {},
			proxy: new Ext.data.HttpProxy({
				ssurl: "/ajax/airports/NULL",
				method: 'GET'
			}),
			root: "tables"
		});
		
		
		config = Ext.apply({
			
			store: this.storeX,
			title: "Tables",
			viewConfig:{
				forceFit: true
			},
			columns: [ 
				{header: "Table", dataIndex: "table"}
			
			],
			listeners:{
				rowclick: {fn: this.row_click, scope: this}
			}
			
			
		}, config);
		
		FGx.DBaseTablesGrid.superclass.constructor.call(this, config);
	},
	
	
	row_click: function(grd, rowIdx, e){
		var table = this.getStore().getAt(rowIdx).get("table");
		console.log("FireEvent: TablesGrid.table=", table);
		this.fireEvent("table", table);
		
		//alert("yes");	
	},
	
	
	load_tables: function(database){
		console.log("TablesGrid.load_tables for db=", database);
		var u = "/ajax/dbase/" + database;
		console.log(u);
		
		this.storeX.load({url: u});
		
	}
	
}); 