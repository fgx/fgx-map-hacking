
FGx.DBaseColumnsGrid = Ext.extend(Ext.grid.GridPanel, {
	
    constructor: function(config) {
		
		
		var store = new Ext.data.JsonStore({
			fields: [	
				{name: "column", type:"string"}
			
			],
			idProperty: "column",
			ssortInfo: {},
			url: "/ajax/dbase",
			root: "columns",
			autoLoad: true
			
		});
		
		
		config = Ext.apply({
			store: store,
			title: "Columns",
			columns: [ 
				{header: "Column", dataIndex: "column"}
			
			]
			
			
		}, config);
		
		FGx.DBaseColumnsGrid.superclass.constructor.call(this, config);
	},
	
	load_columns: function(database, table){
		console.log("Load Columns", database, table);
		var u = "/ajax/dbase/" + database + "/" + table;
		this.getStore().load({url: u});
		console.log(u);
	}
	
}); 