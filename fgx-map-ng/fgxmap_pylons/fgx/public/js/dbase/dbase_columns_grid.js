
FGx.DBaseColumnsGrid = Ext.extend(Ext.grid.GridPanel, {
	
    constructor: function(config) {
		
		
		this.xStore = new Ext.data.JsonStore({
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
		
		
		config = Ext.apply({
			store: this.xStore,
			title: "Columns",
			columns: [ 
				{header: "Column", dataIndex: "column"},
				{header: "Type", dataIndex: "type"},
			
			]
			
			
		}, config);
		
		FGx.DBaseColumnsGrid.superclass.constructor.call(this, config);
	},
	
	load_columns: function( table ){
		//console.log("Load Columns", database, table);
		var u = "/ajax/database/table/" + table + "/columns";
		console.log(u);
		this.xStore.proxy.setUrl(u);
		this.xStore.load();
		//console.log(u);
	}
	
}); 