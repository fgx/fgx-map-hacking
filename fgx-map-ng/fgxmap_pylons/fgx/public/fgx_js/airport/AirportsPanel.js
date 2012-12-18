
Ext.namespace("FGx");
Ext.define("FGx.airport.AirportsPanel", {

extend: "Ext.Panel",
				   
txt_width:60,

action_new_tab: function(){
	if(!this.actionNewTab){
		this.actionNewTab = Ext.create("Ext.Button", {
			text: "New Tab", 
			iconCls: "icoMapGo",
			disabled: true,
			scope: this,
			handler: function(){
				var r = this.get_airports_grid().getSelectionModel().getSelected().data;	
				console.log("OPEN", r);
				//this.fireEvent("OPEN_AIRPORT", r);
				r.lat = r.apt_center_lat;
				r.lon = r.apt_center_lon;
				r.iconCls = "icoAirport";
				r.title = r.apt_ident;
				r.closable = true;
				VP.open_map(r);
			}
		});
	
	}
	return this.actionNewTab;
	
},

//===========================================================
//== Grid
get_airports_grid: function(){
	if(!this.xAirportsGrid){
		this.xAirportsGrid = Ext.create("Ext.grid.GridPanel", {
			region: "center",
			frame: false, plain: true, border: false,
			hideHeader: true,
			autoScroll: true,
			autoWidth: true,
			enableHdMenu: false,
			viewConfig: {
				emptyText: 'No airports in view', 
				deferEmptyText: false,
				forceFit: true
			}, 
			
			stripeRows: true,
			store: this.get_store(),
			loadMask: true,
			tbar: [
				this.action_new_tab()
			],
			columns: [ 
				{header: 'Airport', dataIndex:'apt_ident', sortable: true, flex: 1,
					renderer: function(v, meta, rec){
						return rec.get("apt_ident") + ": " + rec.get("apt_name_ascii");
					}
				}
			]
		});
		this.xAirportsGrid.on("selectionchange", function(selModel, selected, eOpts){
			console.log("selchan");
			//var sm = this.get_airports_grid().getSelectionModel();
			if( selected.length == 0){
				this.action_new_tab().setDisabled(true);
				return;
			}
			this.action_new_tab().setDisabled(false);			
			this.fetch_airport( selected[0].get("apt_ident") );
		}, this);
		
		//this.xAirportsGrid.on("rowdblclick", function(grid, idx, e){
		//	this.fireEvent("OPEN_AIRPORT", grid.getStore().getAt(idx).data);
		//},, this)
	}
	return this.xAirportsGrid;

},

fetch_airport: function(apt_ident){
	Ext.Ajax.request({
		url: "/ajax/airport/" + apt_ident ,
		method: "GET",
		scope: this,
		success: function(response, opts) {
			var data = Ext.decode(response.responseText);
			console.log(data);
			var root = this.get_runways_store().getRootNode();
			root.removeAll();
			
			var runs = data.runways;
			for(var ir = 0; ir < runs.length; ir++){
				var r = runs[ir];
				var rwyNode = Ext.create("mTree", {
						x_key: r.rwy, x_val: r.rwy_length,
						expanded: false,  expandable: true
				});
				root.appendChild(rwyNode);
				for(var it = 0; it < r.thresholds.length; it++){
					var t = r.thresholds[it];
					var tn = new Ext.tree.TreeNode({
						x_key: t.rwy_ident, x_val: "", 
						expanded: false, expandable: true
					})
					rwyNode.appendChild(tn);
					var props = ["rwy_threshold", "rwy_ident", "rwy_reil", "rwy_marking", "rwy_overrun", "rwy_app_lighting"];
					for(var pi =0; pi < props.length; pi++){
						var pk = props[pi];
						var lbl =  pk.replace("rwy_", "");
						lbl = lbl.replace("_", " ");
						var pn = new Ext.tree.TreeNode({
						x_key: lbl, x_val: t[pk], 
						leaf: true
					})
					tn.appendChild(pn);
					}
				}					
			}
		},
		failure: function(response, opts) {
			console.log('server-side failure with status code ' + response.status);
		}
		
	});
},

get_runways_store: function(){
	if(!this.xRunwaysStore){
		this.xRunwaysStore = Ext.create("Ext.data.TreeStore", {
			//model: "mTree",
			root: {
				expanded: true,
				text: "My Root"
			}
		});
	}
	return this.xRunwaysStore;
},

get_runways_tree: function(){
	if(!this.xRunwaysTree){
		this.xRunwaysTree = Ext.create("Ext.tree.Panel", {
			region: "east", autoScroll: true,
			frame: false, plain: true, border: false,
			 useArrows: true,
			 rootVisible: true,
			columns: [
				{xtype: 'treecolumn', header: 'Item', dataIndex: 'x_key', 	flex: 1},
				{header: 'Value', dataIndex: 'x_val', 	flex: 1}
			],
			viewConfig: {
				forceFit: true
			},
			width: 250,
			text: 'Ext JS', 
			store: this.get_runways_store()
			//draggable: false,
			//dataUrl: "/ajax/airport/EGLL",
			
		});
	}
	return this.xRunwaysTree;
},

initComponent: function() {
	Ext.apply(this, {
		iconCls: "icoAirport",
		title: "Airports",
		layout: "border",
		frame: false, plain: true, border: false,
		items: [
			this.get_airports_grid(),
			this.get_runways_tree()		   
		],
		tbar: [	
			{xtype: 'buttongroup', 
				title: 'Find Code',
				columns: 2,
				items: [
					{iconCls: "icoClr",	scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_apt_code_search_text().setValue("");
							this.get_apt_code_search_text().focus();
						}
					},
					this.get_apt_code_search_text()
				]
			},
			{xtype: 'buttongroup', 
				title: 'Find Name',
				columns: 2,
				items: [
					{iconCls: "icoClr",	scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_apt_name_search_text().setValue("");
							this.get_apt_name_search_text().focus();
						}
					},
					this.get_apt_name_search_text()
				]
			},
			{xtype: 'buttongroup', 
				title: 'Show Selected - TODO',
				columns: 5,
				items: [
					{text: "Major", pressed: true, enableToggle: true},
					{text: "Minor", pressed: true, enableToggle: true},
					{text: "Small", enableToggle: true},
					{text: "Water", enableToggle: true},
					{text: "HeliPad", enableToggle: true}
				]
			}
		]
		
	});
	this.callParent();
}, // initComponent

//== Store
get_store: function(){
	if(!this.xStore){
		this.xStore = Ext.create("Ext.data.JsonStore", {
			model: "mAirport",
			proxy: {
				type: "ajax",
				url: '/ajax/airports',
				method: "GET",
				reader: {
					type: "json",
					root: 'airports'
				}
			},
			autoLoad: true,
			
			remoteSort: false,
			sortInfo: {
				field: "apt_ident", 
				direction: 'ASC'
			}
		});
	}
	return this.xStore;
},

get_apt_code_search_text: function(){
	if(!this.txtSearchAptCode){
		this.txtSearchAptCode = new Ext.form.TextField({
			width: this.txt_width,
			enableKeyEvents: true
		});
		this.txtSearchAptCode.on("keyup", function(txtFld, e){
			
				var t = this.get_apt_code_search_text().getValue().trim();
				//t.setValue( t.getValue().trim() );
				//var txt = t.getValue();
				//console.log(t, t.length);
				if(t.length > 1){
					
					this.get_store().load({params: {apt_ident: t}});
				}
				
			
		}, this);
	}
	return this.txtSearchAptCode;
},
get_apt_name_search_text: function(){
	if(!this.txtSearchAptName){
		this.txtSearchAptName = new Ext.form.TextField({
			width: this.txt_width,
			enableKeyEvents: true
		});
		this.txtSearchAptName.on("keyup", function(txtFld, e){
			
				var t = this.get_apt_name_search_text().getValue().trim();
				//t.setValue( t.getValue().trim() );
				//var txt = t.getValue();
				//console.log(t, t.length);
				if(t.length > 2){
					
					this.get_store().load({params: {apt_name_ascii: t}});
				}
				
			
		}, this);
	}
	return this.txtSearchAptName;
}


});

