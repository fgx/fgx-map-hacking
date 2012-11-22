
Ext.namespace("FGx");

FGx.FlightPlansWidget = Ext.extend(Ext.Panel, {

group_renderer: function(v,u,r,rowIndex,colIndex,js){
	return "@" + r.get('ident');
},
	
get_flight_plan_grid: function(){
	if(!this.xFlightPlanGrid){
		this.xFlightPlanGrid = new Ext.grid.GridPanel({
			region: "east",
			width: 300,
			frame: false, plain: true, border: false,
			columns: [
				{header: '#', dataIndex:'idx', sortable: false, align: 'right',
						groupRenderer: this.group_renderer
				},
				{header: 'Ident', dataIndex:'ident', sortable: false, align: 'right',
					groupRenderer: this.group_renderer
				},
				{header: 'Lat', dataIndex:'lat', sortable: false, align: 'right',
				},
				{header: 'Lon', dataIndex:'lon', sortable: false, align: 'right',
				
				},
				{header: 'Type', dataIndex:'nav_type', sortable: false, align: 'right',
				},
				{header: 'Freq', dataIndex:'freq', sortable: false, align: 'right',
				},
			],
			store: new Ext.data.GroupingStore({
				
				//sortInfo: {field: 'idx', direction: "ASC"},
				
				groupField:'idx',
				proxy: new Ext.data.HttpProxy({
					url: "/ajax/database/data/tables",
					method: 'GET'
				}),
				reader: new Ext.data.JsonReader({
					root: "flight_plan",
					fields: [	
						{name: "uid", type:"int"},
						{name: "ident", type:"string"},
						{name: "idx", type:"int"},
						{name: "lat", type:"string"},
						{name: "lon", type:"string"},
						{name: "freq", type:"string"},
						{name: "nav_type", type:"string"}
					],
					idProperty: "uid"
				}),
				
				autoLoad: false
			}),
			loadMask: true,
			view: new Ext.grid.GroupingView({
				forceFit:true,
				ssgroupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})',
				
			}),
			DDDviewConfig:{
				forceFit: true,
				emptyText: "No items to view",
				deferEmptyText: false
			},
		});
		//this.xFlightPlanGrid.on("rowclick", function(grid, rowIdx, e){
		//	var rec = grid.getStore().getAt(rowIdx);
			
			
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
									var data = Ext.decode(response.responseText);
									//this.get_map_panel().load_tracker(obj.tracks);
									console.log(data);
									this.get_flight_plan_grid().getStore().loadData(data)
									
								},
								failure: function(response, opts) {
									console.log('server-side failure with status code ' + response.status);
								}
							});
						}
					}
				]
			},
			new FGx.MapPanel({region: "center"}),
			this.get_flight_plan_grid()
		
		]
		
		
		
		
	}, config);
	FGx.FlightPlansWidget.superclass.constructor.call(this, config);
}, // Constructor	
	
});

