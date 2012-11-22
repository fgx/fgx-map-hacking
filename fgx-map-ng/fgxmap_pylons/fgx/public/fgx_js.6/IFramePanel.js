
Ext.namespace("FGx");

FGx.IFramePanel = Ext.extend(Ext.Panel, {

//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		iconCls: 'icoHelp',
		fgxType: "IFramePanel",
		layout : 'fit',
		closable: true,
		deferredRender : false,
		items : [
			{
			xtype : "component", autoWidth: true,
			autoEl : {
				tag : "iframe",
				src : "http://fgx.ch"
			}
		}
			
		]
		
	}, config);
	FGx.IFramePanel.superclass.constructor.call(this, config);
}, // Constructor	


});

