







//Ext.Ajax.disableCaching = false;







//================================================================
FGx.AirportsBrowser = function (){
	
var self = this;


this.airportsGrid = new FGx.AirportsGrid({region: 'center'});

this.atcGrid = new FGx.ATCGrid({region: 'east', width: 400});


this.airportsGrid.on("airport", function(apt_code){
	self.atcGrid.load(apt_code);
});


//===================================================================
this.tabPanel  = new Ext.Panel({
		layout: 'border',
		renderTo: "widget_div",
		activeTab: 0,
		ssregion: 'center',
		plain: true,
		height: WIDGET_HEIGHT,
		ssplain: true,
		items: [
			this.airportsGrid,
			this.atcGrid
		]
	
});




} // end function cinstructor