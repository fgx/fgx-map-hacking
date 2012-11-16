
Ext.namespace("FGx");
		
FGx.MapPanel = function(){
	
	var self = this;
	
	var xCenterPoint = new OpenLayers.LonLat(939262.20344,5938898.34882);	
	
	var xDisplayProjection = new OpenLayers.Projection("EPSG:4326");
	var xProjection = new OpenLayers.Projection("EPSG:3857");
	
	var xMap = new OpenLayers.Map({
			allOverlays: false,
			units: 'm',
			// this is the map projection here
			projection: xProjection,
			//sphericalMercator: true,
			
			// this is the display projection, I need that to show lon/lat in degrees and not in meters
			displayProjection: xDisplayProjection,
			
			// the resolutions are calculated by tilecache, when there is no resolution parameter but a bbox in
			// tilecache.cfg it shows you resolutions for all calculated zoomlevels in your browser: 
			// by http://yoururltothemap.org/tilecache.py/1.0.0/layername/ etc.
			// (This would not be necessary for 4326/900913 because this values are widely spread in
			// openlayer/osm/google threads, you will find the resolutions there)
			resolutions: RESOLUTIONS,
			
			// I set a max and min resolution, means setting available zoomlevels by default
			maxResolution: 156543.03390624999883584678,
			minResolution: 0.29858214169740676658,
			
			// i.e. maxExtent for EPSG 3572 is derived by browsing the very useful map at
			// http://nsidc.org/data/atlas/epsg_3572.html. I tried to get this values with mapnik2 and
			// proj4, but the values I get back with box2d are not very useful at the moment
			maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
			
			// zoomlevels 0-13 = 14 levels ?
			zoomLevels: 20
	});
	
	function on_nav_toggled(butt, checked){
		butt.setIconClass( checked ? "icoOn" : "icoOff" );
		self.map.getLayersByName(butt.navaid)[0].setVisibility(checked);
	}
	
	FGx.MapPanel.superclass.constructor.call(this, {
		title: "Foo",
		frame: false,
		plain: true,
		border: 0,
		bodyBorder: false,
		region: "center",
			// we do not want all overlays, to try the OverlayLayerContainer
		map: xMap,
		center: xCenterPoint,
		zoom: 5,
		layers: LAYERS,
		
		tbar: [
		
			//== Map Type  
			{xtype: 'buttongroup', 
				title: 'Settings', width: 80, id: "fgx-settings-box", 
				columns: 2,
				items: [
					//{text: "Me", iconCls: "icoCallSign",  
					//	handler: this.on_me , tooltip: "My Settings", disabled: true
					//},
					{text: "Map", toggleHandler: this.on_nav_toggled, iconCls: "icoMapCore", 
						menu: {
							items: [
								{text: "Landmass", group: "map_core", checked: false, xLayer: "ne_landmass",
									handler: this.on_base_layer, scope: this
								},
								{text: "OSM Normal", group: "map_core", checked: false, 
									xLayer: "osm_normal", handler: this.on_base_layer, ddscope: this
								},
								{text: "OSM Light", group: "map_core", checked: true, 
									xLayer: "osm_light", 
									handler: this.on_base_layer, scope: this
								}
							]
						}
					},
					{iconCls: "icoSettings", 
						menu: {
							items: [
								{text: "Mode" ,
									menu: {
										items: [
											{text: "Civilian mode - no military AF or vortac", group: "map_mode", 
												checked: true, xCivMilMode: "civilian", handler: this.on_civmil_mode},
											{text: "Military Mode - only military and vortac - TODO", group: "map_mode", 
												checked: false, xCivMilMode: "military", disabled: true,
												handler: this.on_civmil_mode
											},
											{text: "Both - TODO", group: "map_mode", 
												checked: false, xCivMilMode: "all", disabled: true,
												handler: this.on_civmil_mode
											}
										]
									}
								}
							]
						}
					} 
				]   
			},
			
			{xtype: 'buttongroup',
				title: 'Navigation Aids',
				columns: 5,
				items: [
					{xtype: "splitbutton", text: "VOR", pressed: false, enableToggle: true,  iconCls: "icoOff", navaid: "VOR", 
						toggleHandler: on_nav_toggled,
						menu: {
							items: [
								{text: "Show range - TODO", checked: false, disabled: true}
							]
						}
					},
					{xtype: "splitbutton", text: "DME", enableToggle: true,  iconCls: "icoOff", navaid: "DME", 
						toggleHandler: on_nav_toggled, 
						menu: {
							items: [
								{text: "Show range - TODO", checked: false, disabled: true}
							]
						}
					},
					{text: "NDB&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
						toggleHandler: on_nav_toggled
					},
					{text: "Fix&nbsp;&nbsp;&nbsp;", enableToggle: true, iconCls: "icoOff", navaid: "FIX", 
						toggleHandler: on_nav_toggled
					},
					{text: "VORTAC", enableToggle: true, iconCls: "icoOff", navaid: "NDB", 
						toggleHandler: on_nav_toggled, 
						hidden: true, id: "fgx-vortac"
					}
				]   
			},
			{xtype: 'buttongroup', disabled: true,
				title: 'Airports - TODO', 
				columns: 6,
				items: [
					{text: "Major", enableToggle: true, pressed: true, iconCls: "icoOn", apt: "major", toggleHandler: this.on_apt_toggled},
					{text: "Minor", enableToggle: true, iconCls: "icoOff", apt: "minor", toggleHandler: this.on_apt_toggled},
					{text: "Small", enableToggle: true, iconCls: "icoOff", apt: "small", toggleHandler: this.on_apt_toggled},
					{text: "Military", enableToggle: true, iconCls: "icoOff", apt: "military", toggleHandler: this.on_apt_toggled,
						hidden: true, id: "fgx-mil-airports"},
					{text: "Seaports", enableToggle: true, iconCls: "icoOff", apt: "seaports", toggleHandler: this.on_apt_toggled},
					{text: "Heliports", enableToggle: true, iconCls: "icoOff", apt: "heliports", toggleHandler: this.on_apt_toggled},
				]   
			},		
			"->",
			
		],
		
	});
	
	
	
	
} /* end MapPanel */

Ext.extend(FGx.MapPanel,GeoExt.MapPanel, {
	initComponent: function(){
		FGx.MapPanel.superclass.initComponent.apply(this, arguments);
	},
	onRender: function(){
		FGx.MapPanel.superclass.onRender.apply(this, arguments);
	},
});