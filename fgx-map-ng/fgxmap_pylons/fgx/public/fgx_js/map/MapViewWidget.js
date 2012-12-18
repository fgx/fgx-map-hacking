

Ext.define("FGx.map.MapViewWidget",{

extend: "Ext.Panel", 
W: {
	
},

get_mini_map: function(){
	
	if(!this.xMiniMap){
		this.xMiniMap = new FGx.MiniMapPanel({
			region: "south", height: 250, collapsible: true,
			ddflex: 1,
		});
		
	};
	return this.xMiniMap;
},

get_map_panel: function(){
	if(!this.xMapPanel){
		this.xConfig.region = "center";
		this.xMapPanel =  Ext.create("FGx.map.MapCore", {xConfig: this.xConfig});
	}
	return this.xMapPanel;
},



//======================================================
// Airports Grid
get_airports_grid: function(){
	if(!this.xAirportsGrid){
		
		this.xAirportsGrid =  Ext.create("FGx.airport.AirportsGrid", {});
		this.xAirportsGrid.on("rowclick", function(grid, idx, e){
			var rec = grid.getStore().getAt(idx);
			var r = rec.data
			r.lat = r.apt_center_lat;
			r.lon = r.apt_center_lon;
			console.log(r);
			this.get_mini_map().show_blip(r);
		}, this); 
		this.xAirportsGrid.on("rowdblclick", function(grid, idx, e){
			var rec = grid.getStore().getAt(idx);
			var r = rec.data
			r.lat = r.apt_center_lat;
			r.lon = r.apt_center_lon;
			this.get_map_panel().pan_to( r, 10 );
			//this.get_map().zoomTo( 10 );
		}, this);  
	}
	return this.xAirportsGrid;
},

//======================================================
// Flights Grid
get_flights_grid: function(sto){
	if(!this.xFlightsGrid){
		this.xFlightsGrid =  new FGx.FlightsGrid({
			flightsStore: Ext.StoreMgr.lookup("flights_store"), 
			title: "Flights", xHidden: true
		});
		this.xFlightsGrid.getStore().on("load", function(store, recs, idx){
			this.get_map_panel().update_radar(recs);
		}, this);
		this.xFlightsGrid.on("rowclick", function(grid, idx, e){
			var rec = grid.getStore().getAt(idx);	
			this.get_mini_map().show_blip(rec.data);
		}, this); 
		this.xFlightsGrid.on("rowdblclick", function(grid, idx, e){
			var rec = grid.getStore().getAt(idx);			
			this.get_map_panel().pan_to( rec.data, 10 );
			//this.get_map().zoomTo( 10 );
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
			
			this.get_map_panel().load_airway(recs);
			//console.log("line_pots", line_points);
			this.get_mini_map().show_line(recs);
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
initComponent: function() {
	
	//console.log("constr", config.title, config.lat, config.lon);
	

	Ext.apply(this, {
		
		fgxType: "map_panel",
		iconCls: "icoMap",
		frame: false, plain: true,border: 0,	bodyBorder: false,
		
		layout: "border",
		items: [
			

			this.get_map_panel(),	
				
			{region: 'east', width: 400, 
				collapsible: true,
				collapsed: false,
				frame: false,
				plain: true,
				border: 0,
				layout: "border",
				items: [
					{title: "FGx Map - Next Gen",
						xtype: 'tabpanel', region: "center",
						frame: false,
						plain: true,
						border: 0,
						flex: 2,
						activeItem: 0,
						items: [
							this.get_airports_grid(),
							this.get_nav_widget(),
							this.get_awy_widget(),
							this.get_flights_grid()
						]
					},
		
					this.get_mini_map()
				]
			}
		]
		
		
	});
	this.callParent();
	
}, 



on_goto: function(butt){
	//var lonLat = new OpenLayers.LonLat(butt.lon, butt.lat
	//		).transform(this.get_display_projection(),  this.get_map().getProjectionObject() );
	this.fireEvent("OPEN_MAP", butt.text, true, butt.lon, butt.lat, butt.zoom);
}


});
