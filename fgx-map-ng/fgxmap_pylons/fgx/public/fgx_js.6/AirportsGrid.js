
Ext.namespace("FGx");

FGx.AirportsGrid =  Ext.extend(Ext.Panel, {

//===========================================================
//== Grid
get_airports_grid: function(){
	if(!this.xAirportsGrid){
		this.xAirportsGrid = new Ext.grid.GridPanel({
			region: "center",
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
			columns: [ 
				{header: 'Code',  dataIndex:'apt_ident', sortable: true, 
					width: 60
				},
				
				{header: 'Name', dataIndex:'apt_name_ascii', sortable: true,

				}

			]
		});
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
					var rwysNode = new Ext.tree.TreeNode({
							text: "Runways", expanded: true
							
					});
					root.appendChild(rwysNode);
					for(var i=0; i < data.runways.length; i++){
						var rn = new Ext.tree.TreeNode({
							text: data.runways[0].threshold
						})
						rwysNode.appendChild(rn);
					}
					//this.get_map_panel().load_tracker(obj.tracks);
					
				},
				failure: function(response, opts) {
					console.log('server-side failure with status code ' + response.status);
				}
				
			});
		}, this);
	}
	return this.xAirportsGrid;

},

get_runways_tree: function(){
	if(!this.xRunwaysTree){
		this.xRunwaysTree = new Ext.ux.tree.TreeGrid({
			region: "east", 
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
		items: [
			this.get_airports_grid(),
			this.get_runways_tree()		   
		],
		tbar: [	
			{xtype: 'buttongroup', 
				title: 'Search Code',
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
				title: 'Search Name',
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
			width: 80,
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
			width: 80,
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

