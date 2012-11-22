
Ext.namespace("FGx");

FGx.AirportsGrid =  Ext.extend(Ext.grid.GridPanel, {

//===========================================================
//== Grid
constructor: function(config) {
	config = Ext.apply({
		title: 'Airports',
		iconCls: 'icoAirport',
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
				 width: 100
			},
			
			{header: 'Name', dataIndex:'apt_name_ascii', sortable: true,

			},
			
			{header: 'Authority', dataIndex:'apt_authority', sortable: true, align: 'right'
			},
			{header: 'Size', dataIndex:'apt_size', sortable: true, align: 'right'
			}
		],

		tbar: [	
			{xtype: 'buttongroup', hidden: config.xHidden,
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
			{xtype: 'buttongroup', hidden: config.xHidden,
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
		/*
		bbar: [
			new Ext.PagingToolbar({
				store: this.get_store(),
				displayInfo: false,
				pageSize: 500,
				prependButtons: false
			})
		] */
		
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

