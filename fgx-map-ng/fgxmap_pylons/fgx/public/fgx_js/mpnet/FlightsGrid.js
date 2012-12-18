

Ext.define("FGx.mpnet.FlightsGrid" ,  {

extend: "Ext.grid.Panel",
xHidden: false,
	
//===========================================================
//== Renderers 
// @todo: pete to put in css
render_callsign: function(v, meta, rec){
	return "<b>" + v + "</b>";
},

render_altitude: function(v, meta, rec){
	
	//meta.style = "background-color: XXX";
	
	return Ext.util.Format.number(v, '00,000');	
},

//===========================================================
//== Grid
initComponent: function() {
	Ext.apply(this, {
		sstitle: 'Flights',
		iconCls: 'icoFlights',
		fgxType: "FlightsGrid",
		autoScroll: true,
		autoWidth: true,
		enableHdMenu: false,
		viewConfig: {
			emptyText: 'No flights in view', 
			deferEmptyText: false,
			loadMask: false
		}, 
		stripeRows: true,
		store: Ext.StoreMgr.lookup("flights_store"),
		columns: [ 
			{header: 'CallSign',  dataIndex:'callsign', sortable: true, 
				renderer: this.render_callsign, width: 100, menuDisabled: true
			},
			
			{header: 'Alt', dataIndex:'alt_ft', sortable: true, align: 'right', width: 80,
				renderer: this.render_altitude, menuDisabled: true
			},
			//{header: '', dataIndex:'alt_trend', sortable: true, align: 'center', width: 20,	hidden: true,
			//	renderer: this.render_altitude_trend},
			{header: 'Hdg', dataIndex:'hdg', sortable: true, align: 'right', width: 50, menuDisabled: true,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return v; //Ext.util.Format.number(v, '0');
				}
			},
			{header: 'Spd', dataIndex:'spd_kts', sortable: true, align: 'right', width: 50, menuDisabled: true,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return Ext.util.Format.number(v, '0');
				}
			},
			 {header: 'Lat', dataIndex:'lat', sortable: true, align: 'right', hidden: this.xHidden, menuDisabled: true,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return Ext.util.Format.number(v, '0.00000');
				}
			},
			{header: 'Lon', dataIndex:'lon', sortable: true, align: 'right', hidden: this.xHidden, menuDisabled: true,
				renderer: function(v, meta, rec, rowIdx, colIdx, store){
					return Ext.util.Format.number(v, '0.00000');
				}
			},
			{header: 'Aircraft',  dataIndex:'model', sortable: true, menuDisabled: true,
				flex: 1
			}

		],		
		bbar: [
			new Ext.PagingToolbar({
				hidden: this.xHidden,
				store: Ext.StoreMgr.lookup("flights_store"),
				displayInfo: false,
				pageSize: 500,
				prependButtons: false
			})
		]
		
	});
	this.callParent();
}, // Constructor	



});

