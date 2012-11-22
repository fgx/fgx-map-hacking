
Ext.namespace("FGx");

FGx.FlightPlansWidget = Ext.extend(Ext.Panel, {

group_renderer: function(v,u,r,rowIdx,colIdx, ds){
	console.log(v, u, r, rowIdx, colIdx, ds);
	return r.get('idx') + ": " + r.get('ident');
},
	
get_flight_plan_grid: function(){
	if(!this.xFlightPlanGrid){
		this.xFlightPlanGrid = new Ext.grid.GridPanel({
			region: "east",
			width: 300,
			frame: false, plain: true, border: false,
			columns: [
				{header: '', dataIndex:'idx', sortable: false, align: 'right',
						groupRenderer: this.group_renderer, hidden: true
				},
				{header: 'Ident', dataIndex:'ident', sortable: false, align: 'right',
					ssgroupRenderer: this.group_renderer
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
			enableHdMenu: false,
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
				emptyText: "No items to view",
				deferEmptyText: false,
				ssgroupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "Items" : "Item"]})',
				
			}),
			DDDviewConfig:{
				forceFit: true,
				
			},
		});
		//this.xFlightPlanGrid.on("rowclick", function(grid, rowIdx, e){
		//	var rec = grid.getStore().getAt(rowIdx);
		this.xFlightPlanGrid.getStore().on("load", function(store, recs){
			//console.log(recs);
			/* var recs_length = recs.length;
			
			var fpoints = [];
			for(var i =0; i < recs_length; i++){
				var r = recs[i].data;
				if(r.lat && r.lon){
					fpoints.push(r);
				}
			}*/
			this.get_map_panel().load_flight_plan(recs);
		}, this);
			
	}
	return this.xFlightPlanGrid;
},

get_map_panel: function(){
	if(!this.xMapPanel){
		this.xMapPanel = new FGx.MapPanel({
			region: "center",
		});
	}
	return this.xMapPanel;
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
						ssvalue: "EGLL SID BPK UN866 LEDBO UM604 INBOB M604 SVA Z101 GUBAV Z156 AMIMO P80 LATEN B483 PETAG B954 GIKSI G7 LURET R351 KUMOG G902 FRENK B244 OTZ J502 FAI J515 HRDNG J502 RDFLG J515 ORT J502 YZT J523 TOU J501 OED J1 RBL STAR KSFO",
						ssvalue: "EGLL SID DVR UL9 KONAN UL607 KOK UM150 DIK UN852 GTQ UT3 BLM DCT LSZO",
						value: "EGFF SID EXMOR UM140 DVR UL9 KONAN UL607 AMASI UM149 BOMBI UL984 PADKA L984 DIBED UL984 NM UM991 OLGIN B494 MKL B491 BISNA M23 MARAL B450 BIBIM N644 ABDAN B371 LEMOD N644 DI A466 JHANG M875 KAKID M770 OBMOG L515 IKULA R325 PUT B579 VPL W531 VIH R325 VJB G579 SJ A464 TPG M635 ATMAP A576 PKS H319 TARAL Y59 RIVET STAR YSSY"
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
									//console.log(data);
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
			this.get_map_panel(),
			this.get_flight_plan_grid()
		
		]
		
		
		
		
	}, config);
	FGx.FlightPlansWidget.superclass.constructor.call(this, config);
}, // Constructor	
	
});

