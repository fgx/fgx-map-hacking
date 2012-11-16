
Ext.namespace("FGx");
		
FGx.MapPanel = function(){
	
	FGx.MapPanel.superclass.constructor.call(this, {
		
		title: "FOO",
		
	});
	
	
	
	
} /* end MapPanel */

Ext.extend(FGx.MapPanel, Ext.Panel, {
	initComponent: function(){
		FGx.MapPanel.superclass.initComponent.apply(this, arguments);
	},
	onRender: function(){
		FGx.MapPanel.superclass.onRender.apply(this, arguments);
	},
});