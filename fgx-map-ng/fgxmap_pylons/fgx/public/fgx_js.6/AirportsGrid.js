
Ext.namespace("FGx");

FGx.AirportsGrid =  Ext.extend(Ext.Panel, {

txt_width:60,

action_new_tab: function(){
	if(!this.actionNewTab){
		this.actionNewTab = new Ext.Button({
			text: "New Tab", 
			iconCls: "icoMapGo",
			disabled: true,
			scope: this,
			handler: function(){
				var r = this.get_airports_grid().getSelectionModel().getSelected().data;	
				console.log("OPEN", r);
				this.fireEvent("OPEN_AIRPORT", r);
			}
		});
	
	}
	return this.actionNewTab;
	
},

//===========================================================
//== Grid
get_airports_grid: function(){
	if(!this.xAirportsGrid){
		this.xAirportsGrid = new Ext.grid.GridPanel({
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
			sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
			tbar: [
				this.action_new_tab()
			],
			columns: [ 
				{header: 'Airport', dataIndex:'apt_ident', sortable: true,
					renderer: function(v, meta, rec){
						return rec.get("apt_ident") + ": " + rec.get("apt_name_ascii");
					}

				}
			]
		});
		this.xAirportsGrid.getSelectionModel().on("selectionchange", function(grid, idx, e){
			console.log("selchan");
			var sm = this.get_airports_grid().getSelectionModel();
			if( !sm.hasSelection()){
				this.action_new_tab().setDisabled(true);
				return;
			}
			
			this.action_new_tab().setDisabled(false);			
		}, this);
		this.xAirportsGrid.on("rowclick", function(grid, idx, e){
			var r = grid.getStore().getAt(idx).data;
			Ext.Ajax.request({
				url: "/ajax/airport/" + r.apt_ident ,
				method: "GET",
				scope: this,
				success: function(response, opts) {
					var data = Ext.decode(response.responseText);
					console.log(data);
					var root = this.get_runways_tree().getRootNode();
					root.removeAll();
					
					var runs = data.runways;
					for(var ir = 0; ir < runs.length; ir++){
						var r = runs[ir];
						var rwyNode = new Ext.tree.TreeNode({
								text: r.rwy, expanded: true
						});
						root.appendChild(rwyNode);
						for(var it = 0; it < r.thresholds.length; it++){
							var t = r.thresholds[it];
							var tn = new Ext.tree.TreeNode({
								text: t.rwy_ident
							})
							rwyNode.appendChild(tn);
						}					
					}
				},
				failure: function(response, opts) {
					console.log('server-side failure with status code ' + response.status);
				}
				
			});
		}, this);
		//this.xAirportsGrid.on("rowdblclick", function(grid, idx, e){
		//	this.fireEvent("OPEN_AIRPORT", grid.getStore().getAt(idx).data);
		//},, this)
	}
	return this.xAirportsGrid;

},

get_runways_tree: function(){
	if(!this.xRunwaysTree){
		this.xRunwaysTree = new Ext.ux.tree.TreeGrid({
			region: "east", 
			frame: false, plain: true, border: false,
			columns: [
				{header: 'Item', dataIndex: 'task', 	width: 100	},
				{header: 'Value', dataIndex: 'task', 	swidth: 230	}
			],
			width: 200,
			text: 'Ext JS', 
			draggable: false,
			dataUrl: "/ajax/airport/EGLL",
			ssroot: {
				nodeType: 'async',
				text: 'NA', expandable: true,
				
				draggable: false,
				id: 'rootsss'
				
			}
		});
	}
	return this.xRunwaysTree;
},

constructor: function(config) {
	config = Ext.apply({
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
		
	}, config);
	FGx.AirportsGrid.superclass.constructor.call(this, config);
}, // Constructor	

//== Store
get_store: function(){
	if(!this.xStore){
		this.xStore = new Ext.data.JsonStore({
			idProperty: 'apt_pk',
			fields: [ 	
				{name: "apt_pk", type: 'string'},
				{name: "apt_ident", type: 'string'},
				{name: "apt_name_ascii", type: 'string'},
				{name: "apt_size", type: 'string'},
				{name: "apt_center_lat", type: 'string'},
				{name: "apt_center_lon", type: 'string'},
				{name: "apt_authority", type: 'string'},
			],
			proxy: new Ext.data.HttpProxy({
				url: '/ajax/airports',
				method: "GET",
				params: {apt_ident: "egl"},
			}),
			autoLoad: true,
			root: 'airports',
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

