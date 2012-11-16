
FGx.DBaseTablesGrid = Ext.extend(Ext.grid.GridPanel, {
	
    constructor: function(config) {
		
		
		this.storeX = new Ext.data.JsonStore({
			fields: [	
				{name: "table", type:"string"}
			
			],
			idProperty: "table",
			ssortInfo: {},
			proxy: new Ext.data.HttpProxy({
				url: "/ajax/airports/NULL",
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
		this.fireEvent("TABLE", table);
		
	},
	
	
	load_tables: function(database){
		//console.log("TablesGrid.load_tables for db=", database);
		var u = "/ajax/database/tables";
		//console.log("u=", u);
		this.storeX.proxy.setUrl(u);
		this.storeX.load();
		
	}
	
}); 

