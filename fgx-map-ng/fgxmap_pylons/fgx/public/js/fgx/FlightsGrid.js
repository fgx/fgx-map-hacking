
Ext.namespace("FGx");

FGx.FlightsGrid = Ext.extend(Ext.grid.GridPanel, {

//var self = this,

//this.refresh_rate = 0,
//this.runner = new Ext.util.TaskRunner(),

tbw: 35,

//= Triggered when a refresh toolbar button is clicked
on_refresh_toggled: function(butt, checked){
	butt.setIconClass( checked ? "icoOn" : "icoOff");
	if(checked){
		this.runner.stopAll(); // stop if already ruinning
		this.refresh_rate = parseInt(butt.ref_rate, 10);
		if(this.refresh_rate === 0){
			//this.runner.stop()
		}else{
			this.runner.start( { run: this.update_flights, interval: this.refresh_rate * 1000 });
		}
	}
},

//= Riggered for reshresh now
on_refresh_now: function(){
	this.store.load();
},





	
//===========================================================
//== Renderers 
// @todo: pete to put in css
render_callsign: function(v, meta, rec){
	return "<b>" + v + "</b>";
},

render_altitude: function(v, meta, rec){
	return Ext.util.Format.number(v, '00,000');	
},

//===========================================================
//== Grid
constructor: function(config) {
	
	config = Ext.apply({
		sstitle: 'Flights',
		iconCls: 'icoFlights',
		autoScroll: true,
		autoWidth: true,
		enableHdMenu: false,
		viewConfig: {
			emptyText: 'No flights in view', 
			deferEmptyText: false,
			forceFit: true
		}, 
		stripeRows: true,
		store: config.store,
		loadMask: false,
		sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
		columns: [ 
			//{header: 'F',  dataIndex:'flag', sortable: true, width: 40, hidden: false},
			{header: 'CallSign',  dataIndex:'callsign', sortable: true, 
				renderer: this.render_callsign, width: 100
			},
			
			{header: 'Alt', dataIndex:'alt_ft', sortable: true, align: 'right', width: 80,
				renderer: this.render_altitude
			},
			//{header: '', dataIndex:'alt_trend', sortable: true, align: 'center', width: 20,	hidden: true,
			//	renderer: this.render_altitude_trend},
			{header: 'Hdg', dataIndex:'heading', sortable: true, align: 'right', width: 50,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return v; //Ext.util.Format.number(v, '0');
				}
			},
			{header: 'Spd', dataIndex:'spd_kts', sortable: true, align: 'right',  
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return Ext.util.Format.number(v, '0');
				}
			},
			 {header: 'Lat', dataIndex:'lat', sortable: true, align: 'right', hidden: false,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return Ext.util.Format.number(v, '0.00000');
				}
			},
			{header: 'Lon', dataIndex:'lon', sortable: true, align: 'right', hidden: false,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return Ext.util.Format.number(v, '0.00000');
				}
			},
			{header: 'Server', dataIndex:'server', sortable: true, align: 'left', hidden: false,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return v;
				}
			},
			{header: 'Aircraft',  dataIndex:'model', sortable: true, hidden: false,
				width: 100,
			},

		],
		
		tbar: [	//this.pilotsDataCountLabel
			{xtype: 'buttongroup',
				title: 'Refresh Secs',
				columns: 7,
				items: [
					{text: "Now", iconCls: "icoRefresh",  handler: this.on_refresh_now, scope: this},
					{text: "Off", iconCls: "icoOn", pressed: true, enableToggle: true, scope: this,
						toggleGroup: "ref_rate", ref_rate: 0, toggleHandler: this.on_refresh_toggled},
					{text: "2", iconCls: "icoOff", enableToggle: true,   scope: this, width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 2, toggleHandler: this.on_refresh_toggled},
					{text: "3", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 3, toggleHandler: this.on_refresh_toggled},
					{text: "4", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 4, toggleHandler: this.on_refresh_toggled},
					{text: "5", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 5, toggleHandler: this.on_refresh_toggled},
					{text: "10", iconCls: "icoOff", enableToggle: true,   scope: this, width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 6, toggleHandler: this.on_refresh_toggled}
				]   
			}
		],
		bbar: [
			new Ext.PagingToolbar({
				//frame: false, plain: true, 
				store: config.store,
				displayInfo: true,
				pageSize: 500,
				prependButtons: true	
			})
		]
	}, config);
	FGx.FlightsGrid.superclass.constructor.call(this, config);
} // Constructor	



});

