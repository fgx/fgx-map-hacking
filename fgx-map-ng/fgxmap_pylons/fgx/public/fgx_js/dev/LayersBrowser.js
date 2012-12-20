

//================================================================
Ext.define("FGx.dev.LayersBrowser",  {

extend: "Ext.tab.Panel",

//======================================================
grid_layers: function(){
	if(!this.gridLayers){
		this.gridLayers = Ext.create("Ext.grid.Panel", {
			region: 'center',
			title: "Layer Defs",
			width: 200,
			store:  Ext.create("Ext.data.JsonStore", {
				fields: [	
					{name: "layer", type:"string"},
					{name: "tilecache", type:"string", defaultValue: null},
					{name: "mapnik", type:"string", defaultValue: null},
					{name: "type", type:"string", defaultValue: null},
					{name: "levels", type:"int", defaultValue: null},
					{name: "metabuffer", type:"int", defaultValue: null},
					{name: "openlayers", type:"string"},
				],
				idProperty: "layer",
				proxy: {
					type: "ajax",
					url: "/ajax/map/layers/all",
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
				{header: "Unique", dataIndex: "layer", flex:1, menuDisabled: true,
					renderer: function(val, meta, record, idx){
						meta.style = "font-weight: bold;"
						return val;
					}
				},
				{header: "OpenLayer", dataIndex: "openlayers", flex:1, menuDisabled: true},
				{header: "Tileache", dataIndex: "tilecache", flex:1, menuDisabled: true},
				{header: "Mapnik", dataIndex: "mapnik", flex:1, menuDisabled: true},
				{header: "Type", dataIndex: "type", flex:1, menuDisabled: true},
				{header: "Levels", dataIndex: "levels", flex:1, menuDisabled: true},
				{header: "metabuffer", dataIndex: "metabuffer", flex:1, menuDisabled: true}
				
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
		fgxType: "LayersBrowsers",
		title: "Layers",
		iconCls: "icoDatabase",
		activeTab: 0,
		tbar: [
			
		],
		//height: window.innerHeight - 5,
		items: [
			this.grid_layers(),
			//this.view_tilecache(),
			  {xtype: "panel", title: "Mapnik Config", layout: "fit",
				items: [
					{type: "textfield", name: "resources_xml"}
				]
		   
			  }
		]
	
	});
	this.callParent();
	
},


load:  function(){
	this.grid_layers().getStore().load();
}

});  // end  constructor