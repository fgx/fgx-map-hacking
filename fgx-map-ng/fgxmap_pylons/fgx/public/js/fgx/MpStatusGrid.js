
Ext.namespace("FGx");

FGx.MpStatusGrid = Ext.extend(Ext.grid.GridPanel, {

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
		iconCls: 'icoMpServers',
		autoScroll: true,
		autoWidth: true,
		enableHdMenu: false,
		viewConfig: {
			emptyText: 'No servers in view', 
			deferEmptyText: false,
			forceFit: true
		}, 
		stripeRows: true,
		store: this.get_store(),
		loadMask: false,
		sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
		columns: [ 
			//{header: 'F',  dataIndex:'flag', sortable: true, width: 40, hidden: false},
			{header: 'ip',  dataIndex:'ip', sortable: true, 
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
		
		bbar: [
			new Ext.PagingToolbar({
				//frame: false, plain: true, 
				store: this.get_store(),
				displayInfo: true,
				pageSize: 500,
				prependButtons: true	
			})
		]
	}, config);
	FGx.MpStatusGrid.superclass.constructor.call(this, config);
}, // Constructor	


get_store: function(){
	if(!this.xStore){
		this.xStore = new Ext.data.JsonStore({
			idProperty: 'callsign',
			fields: [ 	{name: 'no', type: 'int'},
						{name: 'fqdn', type: 'string'},
						{name: "ip", type: 'string'},
						{name: "server", type: 'string'},
						{name: "model", type: 'string'},
						{name: "lat", type: 'float'},
						{name: "lon", type: 'float'},
						{name: "alt_ft", type: 'int'},
						{name: "spd_kts", type: 'int'},
						//{name: "alt_trend", type: 'string'},
						{name: "heading", type: 'string'}
			],
			url: '/ajax/mp/status',
			root: 'mpservers',
			remoteSort: false,
			sortInfo: {
				field: "no", 
				direction: 'ASC'
			},
			autoLoad: true,
		});	
	}
	return this.xStore;
}


});

