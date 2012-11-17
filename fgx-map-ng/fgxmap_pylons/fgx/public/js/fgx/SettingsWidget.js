Ext.namespace("FGx");

FGx.SettingsWidget = Ext.extend(Ext.Panel, {

tbw: 50,	
	
//===========================================================
//== Grid
constructor: function(config) {
	
	config = Ext.apply({
		title: 'Settings',
		iconCls: "icoSettings",
		xRunner: config.runner,
		sswidth: 500,
		tbar: [	//this.pilotsDataCountLabel
			{xtype: 'buttongroup',
				title: 'Set Multiplayer Refresh Secs',
				columns: 7,
				items: [
					//{text: "Now", iconCls: "icoRefresh",  handler: this.on_refresh_now, scope: this},
					{text: "Off", iconCls: "icoOff", enableToggle: true, scope: this,
						toggleGroup: "ref_rate", ref_rate: 0, toggleHandler: this.on_refresh_toggled},
					{text: "2", iconCls: "icoOff", enableToggle: true,   scope: this, width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 2, toggleHandler: this.on_refresh_toggled},
					{text: "3", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 3, toggleHandler: this.on_refresh_toggled},
					{text: "4", iconCls: "icoOn", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 4, pressed: true,  toggleHandler: this.on_refresh_toggled},
					{text: "5", iconCls: "icoOff", enableToggle: true,  scope: this,  width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 5, toggleHandler: this.on_refresh_toggled},
					{text: "10", iconCls: "icoOff", enableToggle: true,   scope: this, width: this.tbw,
						toggleGroup: "ref_rate", ref_rate: 6, toggleHandler: this.on_refresh_toggled}
				]   
			}
		],
		
		items: [
			
		]
	}, config);
	
	FGx.SettingsWidget.superclass.constructor.call(this, config);
}, // Constructor	

on_refresh_toggled: function(butt, checked){
	butt.setIconClass( checked ? "icoOn" : "icoOff");
	if(checked){
		//this.xRunner.stopAll(); // stop if already ruinning
		//console.log("yes");
		var refresh_rate = parseInt(butt.ref_rate, 10);
		this.fireEvent("SET_REFRESH", refresh_rate);

		//if(refresh_rate === 0){
		//	this.xRunner.stop()
		//}else{
		//	this.xRunner.start( { run: this.update_flights, interval: refresh_rate * 1000 });
		//}
	}
}

});
