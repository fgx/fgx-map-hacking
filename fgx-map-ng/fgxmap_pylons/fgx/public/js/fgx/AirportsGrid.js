
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
			
			{header: 'Name', dataIndex:'apt_name', sortable: true,

			},
			{header: 'Foo', dataIndex:'email', sortable: true,

			},
			{header: 'Level', dataIndex:'level', sortable: true, align: 'right'
			}
		],

		tbar: [	
			{xtype: 'buttongroup', hidden: config.xHidden,
				title: 'Search',
				columns: 3,
				items: [
					{iconCls: "icoClr",	scope: this, tooltip: "Clear text box",
						handler: function(){
							this.get_apt_search_text().setValue("");
							this.get_apt_search_text().focus();
						}
					},
					this.get_apt_search_text()
				]
			}
		],
		
		bbar: [
			new Ext.PagingToolbar({
				store: this.get_store(),
				displayInfo: false,
				pageSize: 500,
				prependButtons: false
			})
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
				{name: "apt_name", type: 'string'},
				{name: "apt_country", type: 'string'},
				{name: "apt_center_lat", type: 'string'},
				{name: "apt_center_lon", type: 'string'},
			],
			proxy: new Ext.data.HttpProxy({
				url: '/ajax/__SET_IN_CODE__',
				method: "GET"
			}),
			root: 'rows',
			remoteSort: false,
			sortInfo: {
				field: "ident", 
				direction: 'ASC'
			}
		});
	}
	return this.xStore;
},

get_apt_search_text: function(){
	if(!this.txtSearchApt){
		this.txtSearchApt = new Ext.form.TextField({
			width: 80,
			enableKeyEvents: true
		});
		this.txtSearchApt.on("keypress", function(txtFld, e){
			if( e.getKey() == e.ENTER ){
				var t = this.get_ndb_search_text();
				t.setValue( t.getValue().trim() );
				var txt = t.getValue();
				if(txt.length < 2){
					return;
				}
				this.get_store().proxy.setUrl("/ajax/TODO")
				this.get_store().load({params: {q: txt, type: "ndb"}});
			}
		}, this);
	}
	return this.txtSearchApt;
}


});

