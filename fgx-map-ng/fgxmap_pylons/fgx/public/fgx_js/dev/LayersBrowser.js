

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
					{name: "openlayers", type:"string", defaultValue: null},
					{name: "stylename", type:"string", defaultValue: null}
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
				autoLoad: true,
				listeners: {
					scope: this,
					load: function(store, records, success){
						
						return;
						
						// Concept to add resolutaions columns abandoned for now
						var data = store.getProxy().getReader().rawData;
						//console.log(store.getProxy().getReader().rawData);
						var grid = this.grid_layers();
						
						//Ext.getCmp("resources_xml_text").setRawValue(data.tilecache_cfg);
						for(var i = 0; i < 20; i++){
							var col = Ext.create("Ext.grid.column.Column", {
								text: i, flex: 1
							});
							grid.headerCt.insert(grid.columns.length, col);
						}
						grid.getView().refresh();
					}
				}
			}),
			viewConfig:{
				forceFit: true
			},
			columns: [ 
				{header: "Unique", dataIndex: "layer", width:100, menuDisabled: true,
					renderer: function(val, meta, record, idx){
						meta.style = "font-weight: bold;"
						return val;
					}
				},
				{header: "OpenLayer", dataIndex: "openlayers", width:150, menuDisabled: true},
				{text: "Tilecache", menuDisabled: true, columns: [
						{header: "Layer", dataIndex: "tilecache", menuDisabled: true, sortable: true},
						{header: "Levels", dataIndex: "levels", menuDisabled: true, sortable: true},
						{header: "metabuffer", dataIndex: "metabuffer", sflex:1, menuDisabled: true, sortable: true}
					]
				},
				{text: "Mapnik", menuDisabled: true, columns: [
						{header: "Layer", dataIndex: "mapnik", menuDisabled: true, sortable: true},
						{header: "Type", dataIndex: "type", menuDisabled: true, sortable: true},
						{header: "Style", dataIndex: "stylename", menuDisabled: true, sortable: true}
					]
				}

				
			],
			listeners:{
				scope: this,
				TODOselectionchange: function(grid, selection, e){
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
					{xtype: "textarea", name: "resources_xml", id: "resources_xml_text"}
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