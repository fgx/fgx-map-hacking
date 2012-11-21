
Ext.namespace("FGx");

FGx.FlightsViewWidget = Ext.extend(Ext.Panel, {

get_tracks_store: function(){
	if(!this.xTracksStore){
		
		this.xTracksStore =  new Ext.data.JsonStore({
			idProperty: 'wp_id',
			//##storeId: "tracker_store",
			fields: [ 	
				{name: "wp_id", type: 'int'},
				{name: "time", type: 'string'},
				{name: "callsign", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lon", type: 'float'},
				{name: "alt_ft", type: 'int'},
				{name: "spd_kts", type: 'int'},
				{name: "hdg", type: 'int'}
			],
			url: '/ajax/mpnet/tracker/PILOT',
			root: 'tracks',
			remoteSort: false,
			DEADsortInfo: {
				field: "callsign", 
				direction: 'ASC'
			},
			autoLoad: false
		});
		this.xTracksStore.on("load", function(sto, recs){
			this.get_map_panel().load_tracks(recs);
		}, this);
	}
	return this.xTracksStore;
},
	
	
get_flights_grid: function(){
	if(!this.xFlightsGrid){
		this.xFlightsGrid = new FGx.FlightsGrid({
			region: "center",
			frame: false, plain: true, border: false
		});
		this.xFlightsGrid.on("rowclick", function(grid, rowIdx, e){
			var rec = grid.getStore().getAt(rowIdx);
			console.log(rec.data);
			//this.get_tracks_store().proxy.setUrl( "/ajax/mpnet/tracker/" + rec.get("callsign") );
			//this.get_tracks_store().load();
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
