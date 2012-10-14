
Ext.namespace("FGx");

FGx.MainViewport = function(){

this.flightsGrid = new FGx.FlightsGrid();
console.log("GRID+", this.flightsGrid);
	
this.viewport = new Ext.Viewport({
	layout: "border",
	items: [
		this.flightsGrid.grid,
	{
        region: 'center',
        xtype: 'tabpanel', // TabPanel itself has no title
        items: {
            title: 'Default Tab',
            html: 'The first tab\'s content. Others may be added dynamically'
        }
        
	}
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