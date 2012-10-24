//*******************************************************************************
// Core Object
//*******************************************************************************
function FlightsWidget(){

var self = this;



this.render_callsign = function (v, meta, rec){
	return v
	switch(rec.get('flag')){
		case 0: //* pilot is flying
			meta.css = 'fg_pilot_fly';
			break;
		case 1: //* pilot is new
			meta.css = 'fg_pilot_new';
			break;
		default: //* pilot is < 0 = delete timer
			meta.css = 'fg_pilot_dead';
			break;
	}
	return v;
}


//*****************************************
//** Altirude Related
//*****************************************
this.render_altitude = function (v, meta, rec, rowIdx, colIdx, store){
	return "<span style='color:" + self.altitude_color(v) + ";'>" + Ext.util.Format.number(v, '0,000'); + '</span>';
}
this.render_altitude_trend = function (v, meta, rec, rowIdx, colIdx, store){
	return "<img src='" + self.altitude_image(v, rec.get('check') == 1) + "'>";
}
this.altitude_image = function(alt_trend, is_selected){
	var color = is_selected ? 'red' : 'blue';
	if(alt_trend == 'level'){
		return self.icons.level[color];
	}
	return "Foo"
	return alt_trend == 'climb' ? self.icons.climb[color] : self.icons.descend[color];
}
this.altitude_color = function(v){
	if(v < 1000){
		color = 'red';
	}else if(v < 2000){
		color = '#FA405F';
	}else if(v < 4000){
		color = '#A47F24';
	}else if(v < 6000){
		color = '#7FFA40';
	}else if(v < 8000){
		color = '#40FA6E';
	}else if(v < 10000){
		color = '#40FAAA';
	}else if(v < 15000){
		color = '#FA405F';
	}else if(v < 20000){
		color = '#40FAFA';
	}else{
		color = '#331CDC';
	}
	return color;

}
// Store
this.store = new Ext.data.JsonStore({
	idProperty: 'callsign',
	fields: [ 	{name: 'flag', type: 'int'},
				{name: 'check', type: 'int'},
				{name: "callsign", type: 'string'},
				{name: "server", type: 'string'},
				{name: "aircraft", type: 'string'},
				{name: "lat", type: 'float'},
				{name: "lng", type: 'float'},
				{name: "alt", type: 'int'},
				{name: "alt_trend", type: 'string'},
				{name: "hdg", type: 'string'},
				{name: "dist", type: 'string'}
	],
	url: '/ajax/flights',
	root: 'flights',
	remoteSort: false,
	sortInfo: {field: "callsign", direction: 'ASC'}
});
this.load = function(){
	self.store.load({url: '/ajax/flights'});
};


this.grid = new Ext.grid.GridPanel({
	title: 'Flights Data',
	iconCls: 'iconPilots',
	autoScroll: true,
	region: "east",
	width: 400,
	autoWidth: true,
	enableHdMenu: false,
	viewConfig: {emptyText: 'No flights online', forceFit: true}, 
	store: this.store,
	loadMask: true,
	columns: [  //this.selModel,	
		{header: 'F',  dataIndex:'flag', sortable: true, width: 40, hidden: true},
		{header: 'CallSign',  dataIndex:'callsign', sortable: true, renderer: this.render_callsign},
		{header: 'Aircraft',  dataIndex:'aircraft', sortable: true, sssrenderer: this.render_callsign},
		{header: 'Alt', dataIndex:'alt', sortable: true, align: 'right',
			renderer: this.render_altitude
		},
		{header: '', dataIndex:'alt_trend', sortable: true, align: 'center', width: 20,	
			renderer: this.render_altitude_trend},
		{header: 'Hdg', dataIndex:'hdg', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v; //Ext.util.Format.number(v, '0');
			}
		},
		/*
		{header: 'Dist', dataIndex:'dist', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v; //Ext.util.Format.number(v, '0');
			}
		}, */
		{header: 'Speed', dataIndex:'airspeed', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0');
			}
		},
		{header: 'Lat', dataIndex:'lat', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0.00000');
			}
		},
		{header: 'Lng', dataIndex:'lng', sortable: true, align: 'right',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return Ext.util.Format.number(v, '0.00000');
			}
		},
		{header: 'Server', dataIndex:'server', sortable: true, align: 'left',
			renderer: function(v, meta, rec, rowIdx, colIdx, store){
				return v;
			}
		}

	],
	listeners: {},
	
	bbar: [	//this.pilotsDataCountLabel
		{text: 'Refresh', handler: this.load }
	]
});





} // end widget
