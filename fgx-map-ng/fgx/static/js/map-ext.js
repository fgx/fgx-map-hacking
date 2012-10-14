var centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);
//map.setCenter(centerpoint,5);

var mapPanel, tree;
Ext.onReady(function() {
    // create a map panel with some layers that we will show in our layer tree
    // below.
    mapPanel = new GeoExt.MapPanel({
        border: true,
        region: "center",
        // we do not want all overlays, to try the OverlayLayerContainer
        map: new OpenLayers.Map({
								allOverlays: false,
								units: 'm',
								// this is the map projection here
								projection: new OpenLayers.Projection("EPSG:3857"),
								//sphericalMercator: true,
								
								// this is the display projection, I need that to show lon/lat in degrees and not in meters
								displayProjection: new OpenLayers.Projection("EPSG:4326"),
								
								// the resolutions are calculated by tilecache, when there is no resolution parameter but a bbox in
								// tilecache.cfg it shows you resolutions for all calculated zoomlevels in your browser: 
								// by http://yoururltothemap.org/tilecache.py/1.0.0/layername/ etc.
								// (This would not be necessary for 4326/900913 because this values are widely spread in
								// openlayer/osm/google threads, you will find the resolutions there)
								resolutions: [156543.03390624999883584678,78271.51695312499941792339,39135.75847656249970896170,19567.87923828124985448085,9783.93961914062492724042,4891.96980957031246362021,2445.98490478515623181011,1222.99245239257811590505,611.49622619628905795253,305.74811309814452897626,152.87405654907226448813,76.43702827453613224407,38.21851413726806612203,19.10925706863403306102,9.55462853431701653051,4.77731426715850826525,2.38865713357925413263,1.19432856678962706631,0.59716428339481353316,0.29858214169740676658],
								
								// I set a max and min resolution, means setting available zoomlevels by default
								maxResolution: 156543.03390624999883584678,
								minResolution: 0.29858214169740676658,
								
								// i.e. maxExtent for EPSG 3572 is derived by browsing the very useful map at
								// http://nsidc.org/data/atlas/epsg_3572.html. I tried to get this values with mapnik2 and
								// proj4, but the values I get back with box2d are not very useful at the moment
								maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
								
								// zoomlevels 0-13 = 14 levels ?
								zoomLevels: 20
								}
								),
        center: centerpoint,
        zoom: 5,
        layers: [

			new OpenLayers.Layer.WMS( "Natural Earth", 
				"http://map.fgx.ch:81/mapnik/fgxcache.py?", {
				layers: 'fgx_ne_landmass', 
				format: 'image/png', 
				isBaselayer: true 
				}, {
					buffer:0,
					visibility: false
				}
			),
				 
				 
            // create a group layer (with several layers in the "layers" param)
            // to show how the LayerParamLoader works
            new OpenLayers.Layer.WMS("VFR",
                "http://map.fgx.ch:81/mapnik/fgxcache.py?", {
                    layers: [
                        "fgx_850_vor",
                        "fgx_850_dme",
                        "fgx_850_ndb"
                    ],
                    transparent: true,
                    format: "image/png"
                }, {
                    isBaseLayer: false,
                    buffer: 0,
                    // exclude this layer from layer container nodes
                    displayInLayerSwitcher: false,
                    visibility: false
                }
            ),
			
			new OpenLayers.Layer.WMS("IFR",
				"http://map.fgx.ch:81/mapnik/fgxcache.py?", {
					layers: [
						"fgx_850_ils",
						"fgx_850_ils_info",
						"fgx_850_ils_marker"
						],
						transparent: true,
						format: "image/png"
					}, {
						isBaseLayer: false,
						buffer: 0,
						// exclude this layer from layer container nodes
						displayInLayerSwitcher: false,
						visibility: false
				}
			)
				 
        ]
    });

			// create our own layer node UI class, using the TreeNodeUIEventMixin
			var LayerNodeUI = Ext.extend(GeoExt.tree.LayerNodeUI, new GeoExt.tree.TreeNodeUIEventMixin());
			
			// using OpenLayers.Format.JSON to create a nice formatted string of the
			// configuration for editing it in the UI
			var treeConfig = [{
							  nodeType: "gx_baselayercontainer"
							  }, {
							  nodeType: "gx_overlaylayercontainer",
							  expanded: true,
							  // render the nodes inside this container with a radio button,
							  // and assign them the group "foo".
							  loader: {
							  baseAttrs: {
							  radioGroup: "foo",
							  uiProvider: "layernodeui"
							  }
							  }
							  }, {
							  nodeType: "gx_layer",
							  layer: "VFR",
							  isLeaf: false,
							  // create subnodes for the layers in the LAYERS param. If we assign
							  // a loader to a LayerNode and do not provide a loader class, a
							  // LayerParamLoader will be assumed.
							  loader: {
							  param: "LAYERS"
							  }
							  },
							  {
							  nodeType: "gx_layer",
							  layer: "IFR",
							  isLeaf: false,
							  // create subnodes for the layers in the LAYERS param. If we assign
							  // a loader to a LayerNode and do not provide a loader class, a
							  // LayerParamLoader will be assumed.
							  loader: {
							  param: "LAYERS"
							  }
							  }];
			// The line below is only needed for this example, because we want to allow
			// interactive modifications of the tree configuration using the
			// "Show/Edit Tree Config" button. Don't use this line in your code.
			treeConfig = new OpenLayers.Format.JSON().write(treeConfig, true);
			
			// create the tree with the configuration from above
			tree = new Ext.tree.TreePanel({
										  border: true,
										  region: "west",
										  title: "Layers",
										  width: 200,
										  split: true,
										  collapsible: true,
										  collapseMode: "mini",
										  autoScroll: true,
										  plugins: [
													new GeoExt.plugins.TreeNodeRadioButton({
																						   listeners: {
																						   "radiochange": function(node) {
																						   alert(node.text + " is now the active layer.");
																						   }
																						   }
																						   })
													],
										  loader: new Ext.tree.TreeLoader({
																		  // applyLoader has to be set to false to not interfer with loaders
																		  // of nodes further down the tree hierarchy
																		  applyLoader: false,
																		  uiProviders: {
																		  "layernodeui": LayerNodeUI
																		  }
																		  }),
										  root: {
										  nodeType: "async",
										  // the children property of an Ext.tree.AsyncTreeNode is used to
										  // provide an initial set of layer nodes. We use the treeConfig
										  // from above, that we created with OpenLayers.Format.JSON.write.
										  children: Ext.decode(treeConfig)
										  // Don't use the line above in your application. Instead, use
										  //children: treeConfig
										  
										  },
										  listeners: {
										  "radiochange": function(node){
										  alert(node.layer.name + " is now the the active layer.");
										  }
										  },
										  rootVisible: false,
										  lines: false,
										  bbar: [{
												 text: "Show/Edit Tree Config",
												 handler: function() {
												 treeConfigWin.show();
												 Ext.getCmp("treeconfig").setValue(treeConfig);
												 }
												 }]
										  });
			
			// dialog for editing the tree configuration
			var treeConfigWin = new Ext.Window({
											   layout: "fit",
											   hideBorders: true,
											   closeAction: "hide",
											   width: 300,
											   height: 400,
											   title: "Tree Configuration",
											   items: [{
													   xtype: "form",
													   layout: "fit",
													   items: [{
															   id: "treeconfig",
															   xtype: "textarea"
															   }],
													   buttons: [{
																 text: "Save",
																 handler: function() {
																 var value = Ext.getCmp("treeconfig").getValue()
																 try {
																 var root = tree.getRootNode();
																 root.attributes.children = Ext.decode(value);
																 tree.getLoader().load(root);
																 } catch(e) {
																 alert("Invalid JSON");
																 return;
																 }
																 treeConfig = value;
																 treeConfigWin.hide();
																 }
																 }, {
																 text: "Cancel",
																 handler: function() {
																 treeConfigWin.hide();
																 }
																 }]
													   }]
											   });
			
			new Ext.Viewport({
							 layout: "fit",
							 hideBorders: true,
							 items: {
							 layout: "border",
							 deferredRender: false,
							 items: [mapPanel, tree, {
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
			});