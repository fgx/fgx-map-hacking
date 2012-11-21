
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
		xType: "mpstatus",
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
			{header: 'No',  dataIndex:'no', sortable: true, width: 40},
			{header: 'Domain',  dataIndex:'fqdn', sortable: true
			},
			{header: 'IP Address',  dataIndex:'ip', sortable: true
			},
			
			{header: 'Last Checked', dataIndex:'last_checked', sortable: true, align: 'right',
			},
			{header: 'Last Seen', dataIndex:'last_seen', sortable: true, align: 'right',
			},
			{header: 'Last Lag', dataIndex:'lag', sortable: true, align: 'right',
				renderer: function(v){
					if(v > 0){
						return v;
					}
					return "-";
				}
			},
			{header: 'Country',  dataIndex:'country', sortable: true, hidden: false,
				width: 100,
			},
			{header: 'Time Zone',  dataIndex:'time_zone', sortable: true, hidden: false,
				width: 100,
			},
			{header: 'Status',  dataIndex:'status', sortable: true, hidden: false,
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
			fields: [ 	
				{name: 'no', type: 'int'},
				{name: 'fqdn', type: 'string'},
				{name: "ip", type: 'string'},
				{name: "last_checked", type: 'string'},
				{name: "last_seen", type: 'string'},
				{name: "lag", type: 'int'},
				'country', 'time_zone', 'lat', 'lon'
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

