
FGx.DBaseDatabasesGrid = Ext.extend(Ext.grid.GridPanel, {
	
    constructor: function(config) {
		
		
		var store = new Ext.data.JsonStore({
			fields: [	
				{name: "database", type:"string"}
			
			],
			idProperty: "database",
			ssortInfo: {},
			url: "/ajax/dbase",
			root: "databases",
			autoLoad: true
			
		});
		
		
		config = Ext.apply({
			store: store,
			title: "Databases",
			viewConfig: {
				forceFit: true				
			},
			columns: [ 
				{header: "Database", dataIndex: "database"}
			],
			listeners:{
				rowclick: {fn: this.row_click, scope: this}
			}
			
			
		}, config);
		
		FGx.DBaseDatabasesGrid.superclass.constructor.call(this, config);
	},
	
	row_click: function(grd, rowIdx, e){
		var database = this.getStore().getAt(rowIdx).get("database");
		console.log("FireEvent: DatabasesGrid=database", database);
		this.fireEvent("database", database);
	}
	
}); 