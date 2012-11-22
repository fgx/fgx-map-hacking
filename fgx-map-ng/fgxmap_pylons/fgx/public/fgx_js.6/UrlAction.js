
Ext.namespace("FGx");

FGx.UrlAction = Ext.extend(Ext.Action, {

//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		iconCls: config.icoCls ? config.icoCls : "icoHtml",
		
		menu: [
			{text: "with Desktop Browser"},
			{text: "Open In Tab"}
		]
			
		
		
	}, config);
	FGx.UrlAction.superclass.constructor.call(this, config);
}, // Constructor	


});
