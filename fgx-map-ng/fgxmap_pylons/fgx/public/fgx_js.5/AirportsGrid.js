
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
				
				//{header: 'Authority', dataIndex:'apt_authority', sortable: true, align: 'right'
				//},
				//{header: 'Size', dataIndex:'apt_size', sortable: true, align: 'right'
				//}
			],

			
			/*
			bbar: [
				new Ext.PagingToolbar({
					store: this.get_store(),
					displayInfo: false,
					pageSize: 500,
					prependButtons: false
				})
			] */
			
		});
	}
	return this.xAirportsGrid;

},

get_runways_tree: function(){
	if(!this.xRunwaysTree){
		this.xRunwaysTree = new Ext.tree.TreePanel({
			region: "east",
			width: 200,
			  text: 'Ext JS', 
                draggable:false, // disable root node dragging
				root: {
					nodeType: 'async',
					text: 'Ext JS',
					draggable: false,
					id: 'source'	
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
			idProperty: 'callsign',
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
				method: "GET"
			}),
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

