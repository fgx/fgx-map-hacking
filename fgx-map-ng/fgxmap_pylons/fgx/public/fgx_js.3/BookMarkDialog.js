Ext.namespace("FGx");

FGx.BookMarkDialog = Ext.extend(Ext.Window, {


constructor: function(config) {
	
	config = Ext.apply({
		title: 'BookMark',
		width: 500,
		items: [
			this.get_form()
		]
	}, config);
	
	FGx.BookMarkDialog.superclass.constructor.call(this, config);
}, // Constructor	

get_form: function(){
	if(!this.xForm){
		this.xForm = new Ext.form.FormPanel({
			frame: true, border: 0,
			defaults: {
				
				labelWidth: 100
			},
			bodyStyle: "padding: 50px",
			items: [
				{fieldLabel: "Name", xtype: "textfield", width: 200, name: "name"},
				{fieldLabel: "Lat", xtype: "textfield", width: 50, name: "lat"},
				{fieldLabel: "Lon", xtype: "textfield", width: 50, name: "lon"},
				{fieldLabel: "Zoom", xtype: "numberfield", width: 30, name: "zoom"}
			],
			
			buttons: [
				{text: "Cancel", iconCls: "icoCancel", xtype: "button", scope: this, 
					handler: function(){
						this.close();
					}
				},
				{text: "Save -TODO", iconCls: "icoSave", xtype: "button", scope: this,
					handler: function(){
						this.close();
					}
				}
			]
			
		});
		
	}
	return this.xForm;
},

run_show: function(){
	this.show();
	
}

});
