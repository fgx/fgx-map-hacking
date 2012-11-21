
Ext.namespace("FGx");

FGx.FlightsViewWidget = Ext.extend(Ext.Panel, {

get_flights_grid: function(){
	if(!this.xFlightsGrid){
		this.xFlightsGrid = new FGx.FlightsGrid({
			region: "center"
		});
	}
	return this.xFlightsGrid;
},
get_map_panel: function(){
	if(!this.xMapPanel){
		this.xMapPanel = new FGx.MapPanel({
			region: "center"
		});
	}
	return this.xMapPanel;
},

	
//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		layout: "border",
		iconCls: "icoFlights",
		items: [
			this.get_flights_grid(),
			//{xtype: "panel", region: "center", layout: "region",
			//	items: [
					//this.get_map_panel()
			//	]
			//}
			
			
		
		]

	}, config);
	FGx.FlightsViewWidget.superclass.constructor.call(this, config);
}, // Constructor	



});

 //< FGx.FlightsViewWidget
