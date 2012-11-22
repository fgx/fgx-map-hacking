
Ext.namespace("FGx");

FGx.FlightPlansWidget = Ext.extend(Ext.Panel, {
	
get_flight_plan_grid: function(){
	if(!this.xFlightPlanGrid){
		this.xFlightPlanGrid = new Ext.grid.GridPanel({
			region: "center",
			frame: false, plain: true, border: false
		});
		this.xFlightPlanGrid.on("rowclick", function(grid, rowIdx, e){
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
	return this.xFlightPlanGrid;
},

//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		sstitle: 'Flights',
		iconCls: 'icoFlightPlans',
		fgxType: "FlightPlansWidget",
		layout: "border",
		
		items: [
			{region: "north", xtype: "panel", 
				collapsible: true, collapseFirst: true, ssheight: 150,
				title: "Paste Plan", 
				tbar: [
					//{xtype: "fieldset", title: "Paste Flight Plan", autoHeight: true,
						//items:[
							{xtype: "textarea", width: "90%", id: this.getId() + "flight_plan_paste",
							hideLabel: true, width: window.innerWidth - 100, height: 50,
						value: "EGLL SID BPK UN866 LEDBO UM604 INBOB M604 SVA Z101 GUBAV Z156 AMIMO P80 LATEN B483 PETAG B954 GIKSI G7 LURET R351 KUMOG G902 FRENK B244 OTZ J502 FAI J515 HRDNG J502 RDFLG J515 ORT J502 YZT J523 TOU J501 OED J1 RBL STAR KSFO"
					},
					{text: "Process", iconCls: "icoExecute", scope: this,
						handler: function(){
							Ext.Ajax.request({
								url: "/ajax/flightplan/process",
								method: "POST",
								params: {raw_text: Ext.getCmp(this.getId() + "flight_plan_paste").getValue()},
								scope: this,
								success: function(response, opts) {
									var obj = Ext.decode(response.responseText);
									//this.get_map_panel().load_tracker(obj.tracks);
									
								},
								failure: function(response, opts) {
									console.log('server-side failure with status code ' + response.status);
								}
							});
						}
					}
				]
			},
			new FGx.MapPanel({region: "center"})
		
		]
		
		
		
		
	}, config);
	FGx.FlightPlansWidget.superclass.constructor.call(this, config);
}, // Constructor	
	
});

