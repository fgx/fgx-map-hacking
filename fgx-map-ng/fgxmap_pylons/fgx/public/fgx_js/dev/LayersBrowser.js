

//================================================================
Ext.define("FGx.dev.LayersBrowser",  {

extend: "Ext.Panel",

//======================================================
grid_layers: function(){
	if(!this.gridLayers){
		this.gridLayers = Ext.create("Ext.grid.Panel", {
			region: 'center',
			title: "Layers",
			width: 200,
			store:  new Ext.data.JsonStore({
				fields: [	
					{name: "layer", type:"string"}
				],
				idProperty: "layer",
				
				proxy: {
					type: "ajax",
					url: "/ajax/map/layers",
					method: 'GET',
					reader: {
						type: "json",
						root: "layers"
					}
				},
				autoLoad: true
			}),
			viewConfig:{
				forceFit: true
			},
			columns: [ 
				{header: "Layer", dataIndex: "layer", flex:1, menuDisabled: true,
					renderer: function(val, meta, record, idx){
						meta.style = "font-weight: bold;"
						return val;
					}
				}
				//{header: "rows", dataIndex: "rows"}
			],
			listeners:{
				scope: this,
				selectionchange: function(grid, selection, e){
					return
					
				}
			}
		});
	}
	return this.gridLayers;
},





initComponent: function() {
	
	Ext.apply(this, {
		layout: 'border',
		fgxType: "DbBrowser",
		title: "DB Schema",
		iconCls: "icoDatabase",
		activeTab: 0,
		tbar: [
			
		],
		//height: window.innerHeight - 5,
		items: [
			this.grid_layers(),
			
		]
	
	});
	this.callParent();
	
},

//this.tablesGrid.load_tables();
load:  function(){
	this.grid_tables().getStore().load();
}

});  // end function cinstructor