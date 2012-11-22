
Ext.namespace("FGx");

FGx.UrlAction = Ext.extend(Ext.Action, {

//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		iconCls: config.icoCls ? config.icoCls : "icoHtml",
		
		menu: [
			{text: "Open in desktop"},
			{text: "Open in embedded iframe tab"}
		]
			
		
		
	}, config);
	FGx.UrlAction.superclass.constructor.call(this, config);
}, // Constructor	


});
