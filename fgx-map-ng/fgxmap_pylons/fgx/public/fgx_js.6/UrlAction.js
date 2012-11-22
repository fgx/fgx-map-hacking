
Ext.namespace("FGx");

FGx.UrlAction = Ext.extend(Ext.Action, {

//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		iconCls: config.icoCls ? config.icoCls : "icoHtml",
		
		menu: [
			{text: "Open in desktop", xMode: "window", handler: config.M.on_url_action, scope: M},
			{text: "Open in iframe tab", xMode: "tab", handler: config.M.on_url_action, scope: M}
		]
	}, config);
	FGx.UrlAction.superclass.constructor.call(this, config);
}, // Constructor	


});
