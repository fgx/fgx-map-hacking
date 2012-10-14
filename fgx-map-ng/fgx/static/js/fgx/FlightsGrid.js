
Ext.namespace("FGx");

FGx.FlightsGrid = function(){

//== Store
this.store = mew Ext.data.jsonStore({
	root: "flights",
	fields: [
		{name: 'callsign', type: "string"},
		{name: 'lat', type: "string"},
		{name: 'lon', type: "string"}
	]
});


//== Grid
this.grid = new Ext.grid.GridPanel({
	
	viewConfig: {
		forceFit: true, 
		scrollOffset: 0
	},
	columns: [
		{header: "Callsign", width: 90},
		{header: "Altitude", width: 90},
		{header: "Heading", width: 90}
	],

		
});
	
	
} //< FGx.FlightsGrid
