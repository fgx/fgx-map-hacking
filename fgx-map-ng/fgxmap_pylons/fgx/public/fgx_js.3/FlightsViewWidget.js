
Ext.namespace("FGx");

FGx.FlightsViewWidget = Ext.extend(Ext.Panel, {

	
get_flights_grid: function(){
	if(!this.xFlightsGrid){
		this.xFlightsGrid = new FGx.FlightsGrid({
			region: "center",
			frame: false, plain: true, border: false
		});
		this.xFlightsGrid.on("rowclick", function(grid, rowIdx, e){
			var rec = grid.getStore().getAt(rowIdx);
			
			Ext.Ajax.request({
				url: "/ajax/mpnet/tracker/" + rec.get("callsign"),
				method: "GET",
				scope: this,
				success: function(response, opts) {
					var obj = Ext.decode(response.responseText);
					this.get_map_panel().load_tracker(obj.tracks);
					
				},
				failure: function(response, opts) {
					console.log('server-side failure with status code ' + response.status);
				}
				
			});
			
		}, this);
	}
	return this.xFlightsGrid;
},
get_map_panel: function(){
	if(!this.xMapPanel){
		this.xMapPanel = new FGx.MapPanel({
			region: "east", width: "50%",
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
			//{xtype: "panel", region: "east", layout: "vbox",
			//	width: 400,
			//	items: [
					this.get_map_panel()
			//	]
			//}
			
			
		
		]

	}, config);
	FGx.FlightsViewWidget.superclass.constructor.call(this, config);
}, // Constructor	



});

 //< FGx.FlightsViewWidget
