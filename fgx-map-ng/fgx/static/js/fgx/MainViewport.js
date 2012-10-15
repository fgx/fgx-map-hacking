
Ext.namespace("FGx");

FGx.MainViewport = function(){

this.flightsGrid = new FGx.FlightsGrid();
	
this.viewport = new Ext.Viewport({
	layout: "border",
	plain: true,
	items: [

		{ region: 'center',
			xtype: 'tabpanel', // TabPanel itself has no title
			items: {
				title: 'Default Tab',
				html: 'The first tab\'s content. Others may be added dynamically'
			}
        
		},
		{region: 'east', width: 300, title: "FGx Map - Next Gen",
			xtype: 'tabpanel',
			activeItem: 0,
			items: [
				this.flightsGrid.grid,
				
			]
        
		},
	]
})
	
	
} //< FGx.MainViewport
/*
new Ext.Viewport({
	 layout: "fit",
	 hideBorders: true,
	 items: {
		 layout: "border",
		 deferredRender: false,
		 items: [
		    mapPanel, 
		    tree, 
		    {
			 contentEl: "desc",
		 region: "east",
		 bodyStyle: {"padding": "5px"},
		 collapsible: true,
		 collapseMode: "mini",
		 split: true,
		 width: 200,
		 title: "Description"
			 }]
	 }
 });
 */