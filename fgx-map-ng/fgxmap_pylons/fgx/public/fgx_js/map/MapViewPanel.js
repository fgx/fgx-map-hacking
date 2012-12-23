

Ext.define("FGx.map.MapViewPanel",{

extend: "Ext.Panel", 
W: {
	
},

get_mini_map: function(){
	if(!this.xMiniMap){
		this.xMiniMap = Ext.create("FGx.map.MapMini", {
			region: "south", height: 250, collapsible: true,
			ddflex: 1, xConfig: this.xConfig
		});
		
	};
	return this.xMiniMap;
},

get_main_map: function(){
	if(!this.xMapPanel){
		this.xMapPanel =  Ext.create("FGx.map.MapBasic", {
			xConfig: this.xConfig, flex: 1, region: "center"
		});
	}
	return this.xMapPanel;
},



//======================================================
// Airports Grid
get_airports_panel: function(){
	if(!this.xAirportsPanel){
		
		this.xAirportsPanel =  Ext.create("FGx.airport.AirportsPanel", {});
		this.xAirportsPanel.on("rowclick", function(grid, idx, e){
			var rec = grid.getStore().getAt(idx);
			var r = rec.data
			r.lat = r.apt_center_lat;
			r.lon = r.apt_center_lon;
			console.log(r);
			this.get_mini_map().show_blip(r);
		}, this); 
		this.xAirportsPanel.on("rowdblclick", function(grid, idx, e){
			var rec = grid.getStore().getAt(idx);
			var r = rec.data
			r.lat = r.apt_center_lat;
			r.lon = r.apt_center_lon;
			this.get_map_panel().pan_to( r, 10 );
			//this.get_map().zoomTo( 10 );
		}, this);  
	}
	return this.xAirportsPanel;
},

//======================================================
// Flights Grid
get_flights_grid: function(sto){
	if(!this.xFlightsGrid){
		this.xFlightsGrid =  Ext.create("FGx.mpnet.FlightsGrid", {
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
		
		this.xNavWidget =  Ext.create("FGx.nav.NavWidget", {});
		this.xNavWidget.on("GOTO", function(obj){
			this.get_mini_map().show_blip(obj);
			this.get_map_panel().show_blip(obj);
		}, this);  
			
	}
	return this.xNavWidget;
},

get_awy_widget: function(){
	if(!this.xAwyWidget){
		
		this.xAwyWidget =  Ext.create("FGx.nav.AirwaysPanel", {});
		
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
		frame: false, border: false,	bodyBorder: false,
		
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
					{xtype: 'tabpanel', region: "center",
						frame: false,
						border: false,
						flex: 2,
						activeTab: 1,
						items: [
							this.get_airports_panel(),
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
