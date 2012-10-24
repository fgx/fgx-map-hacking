
FGx.ATCGrid = Ext.extend(Ext.grid.GridPanel, {
	
    constructor: function(config) {
		
		
		var store = new Ext.data.JsonStore({
			
			url: "/ajax/"
		});
		
		
		config = Ext.apply({
			store: store,
			columns: [ {header: "Type"}
			
			]
			
			
		}, config);
		
		FGx.ATCGrid.superclass.constructor.call(this, config);
	},
	
	
	load: function(apt_code){
		var u = "/ajax/airport/" + apt_code + "/atc";
		console.log("Load ATC:", apt_code, u);
		this.getStore().load({url: u});	
		
	}
	
}); 