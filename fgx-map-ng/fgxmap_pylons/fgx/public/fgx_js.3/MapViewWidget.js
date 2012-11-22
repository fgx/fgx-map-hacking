

Ext.namespace("FGx");

FGx.MapViewWidget = Ext.extend(Ext.Panel, {


W: {
	
},

get_mini_map: function(){
	
	if(!this.xMiniMap){
		this.xMiniMap = new FGx.MiniMapPanel({region: "south", height: 300, collapsible: true});
		
	};
	return this.xMiniMap;
},

get_map_panel: function(){
	if(!this.xMapPanel){
		this.xMapPanel =  new FGx.MapPanel({
			region: "center"
		});
	}
	return this.xMapPanel;
},



//======================================================
// Airports Grid
get_airports_grid: function(){
	if(!this.xAirportsGrid){
		
		this.xAirportsGrid =  new FGx.AirportsGrid({});
		/*
		this.xAirportsGrid.on("rowdblclick", function(grid, idx, e){

			var rec = grid.getStore().getAt(idx);
			var lonLat = new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")
				).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	
			this.get_map().setCenter( lonLat );
			this.get_map().zoomTo( 10 );
		}, this);  
		*/		
	}
	return this.xAirportsGrid;
},

//======================================================
// Flights Grid
get_flights_grid: function(sto){
	if(!this.xFlightsGrid){
		this.xFlightsGrid =  new FGx.FlightsGrid({
			//flightsStore: Ext.StoreMgr.lookup("flights_store"), 
			title: "Flights", xHidden: true
		});
		this.xFlightsGrid.getStore().on("load", function(store, recs, idx){
			this.flightLabelsLayer.removeAllFeatures();
			this.flightMarkersLayer.removeAllFeatures();
			var recs_length = recs.length;
			for(var i = 0; i < recs_length; i++){
				var rec = recs[i];
				this.show_radar (rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("alt_ft") );
			};
		}, this);
		this.xFlightsGrid.on("rowdblclick", function(grid, idx, e){

			var rec = grid.getStore().getAt(idx);
			var lonLat = new OpenLayers.LonLat(rec.get("lon"), rec.get("lat")
				).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	
			this.get_map().setCenter( lonLat );
			this.get_map().zoomTo( 10 );
		}, this);  
				
	}
	return this.xFlightsGrid;
},

get_nav_widget: function(){
	if(!this.xNavWidget){
		
		this.xNavWidget =  new FGx.NavWidget({});
		this.xNavWidget.on("GOTO", function(obj){

			this.get_mini_map().show_blip(obj);
			this.get_map_panel().show_blip(obj);
		}, this);  
			
	}
	return this.xNavWidget;
},

get_awy_widget: function(){
	if(!this.xAwyWidget){
		
		this.xAwyWidget =  new FGx.AirwaysPanel({});
		
		this.xAwyWidget.grid_segments().getStore().on("load", function(store, recs, idx){
			//this.flightLabelsLayer.removeAllFeatures();
			//this.flightMarkersLayer.removeAllFeatures();
			//var recs_length = recs.length;
			//for(var i = 0; i < recs_length; i++){
			//	var rec = recs[i];
			//	this.show_radar (rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), //rec.get("alt_ft") );
			//};
			this.get_map_panel().load_airway(recs);
		}, this);
				
		this.xAwyWidget.on("GOTO", function(obj){

			this.get_mini_map().show_blip(obj);
			this.get_map_panel().show_blip(obj);
		}, this);  
			
	}
	return this.xAwyWidget;
},
	
//===========================================================
//== CONSTRUCT
constructor: function(config) {
	
	//console.log("constr", config.title, config.lat, config.lon);
	

	config = Ext.apply({
		
		fgxType: "map_panel",
		iconCls: "icoMap",
		frame: false, plain: true,border: 0,	bodyBorder: false,
		
		layout: "border",
		items: [
			

			this.get_map_panel(),	
				
			{region: 'east', width: 400, 
				layout: "border",
				items: [
					{title: "FGx Map - Next Gen",
						xtype: 'tabpanel', region: "center", 
						frame: false,
						plain: true,
						border: 0,
						collapsible: true,
						collapsed: false,
						activeItem: 0,
						items: [
							this.get_awy_widget(),
							this.get_nav_widget(),
							this.get_airports_grid(),
							
							this.get_flights_grid()
							
						]
					},
					this.get_mini_map()
				]
			}
		]
		
		
	}, config);
	FGx.MapViewWidget.superclass.constructor.call(this, config);

	
}, // Constructor	



init: function(){

	
	//this.get_map().addLayer( this.highLightMarkers );
	//this.get_map().addLayer( this.flightMarkersLayer );
	//this.get_map().addLayer( this.flightLabelsLayer );
	
	//this.set_base_layer("Dark"); //??? WTF!!
	
	DEADthis.get_flights_grid().getStore().on("load", function(store, recs, idx){
		console.log("YESSSSS");
		this.flightLabelsLayer.removeAllFeatures();
		this.flightMarkersLayer.removeAllFeatures();
		var recs_length = recs.length;
		for(var i = 0; i < recs_length; i++){
			var rec = recs[i];
			this.show_radar (rec.get("callsign"), rec.get("lat"), rec.get("lon"), rec.get("heading"), rec.get("alt_ft") );
		};
	}, this);
},


on_goto: function(butt){
	//var lonLat = new OpenLayers.LonLat(butt.lon, butt.lat
	//		).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	this.fireEvent("OPEN_MAP", butt.text, true, butt.lon, butt.lat, butt.zoom);
}


});
