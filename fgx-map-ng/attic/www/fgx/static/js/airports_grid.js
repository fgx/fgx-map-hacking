


//================================================================
FGx.AirportsGrid = Ext.extend(Ext.grid.GridPanel, {
	
    initComponent: function() {
		
		Ext.apply(this, {
			
			title: 'Airports',
			region: 'center',
			ssiconCls: 'iconPilots',
			autoScroll: true,
			autoWidth: true,
			enableHdMenu: false,
			viewConfig: {
				emptyText: 'No airports', 
				forceFit: true
			}, 
			store: this.get_store(),
			loadMask: true,
			columns: [  //this.selModel,	
				{header: 'Apt ICAO',  dataIndex:'apt_icao', sortable: true},
				{header: 'Apt Name',  dataIndex:'apt_name', sortable: true}
			],
			tbar:[
				{text: 'APT Code'},
				new Ext.form.TextField({
					allowBlank: false,
					emptyText: "code",
					enableKeyEvents: true,
					minLength: 2,
					maxLength: 4,
					listeners:{
						keydown: {fn: this.on_search_icao, scope: this}
					}
				}),
				'-',
			
				{text: 'APT Name'},
				new Ext.form.TextField({
					allowBlank: false,
					emptyText: "search name",
					enableKeyEvents: true,
					minLength: 2,
					maxLength: 4,
					listeners:{
						keydown: {fn: this.on_search_name, scope: this}
					}
				}),
				'-',

				new Ext.form.Checkbox({
					inputValue: 1,
					boxLabel: 'Only Major Airports',
					ref: "../chkBoxICAO"
	
				})
			],
	
			bbar: [
			new Ext.PagingToolbar({
				store: this.get_store(),      
				displayInfo: true,
				displayMsg: "Airports {0} - {1} of {2}",
				emptyMsg: "No airports in this view",
				pageSize: 100,
				prependButtons: false
			})
			]
		});
		FGx.AirportsGrid.superclass.initComponent.call(this); 
	}, /* initComponent */


	load: function(){
		this.getStore.load();
	},
	

	
	on_search_icao: function(fld, e){
		if( e.getKey() == e.ENTER ){
			var v = fld.getValue();
			var c = this.chkBoxICAO.getValue() == 1 ? 1 : 0;
			this.getStore().load({params: {apt_icao: v, icao_only: c}});
		}
	},
	on_search_name: function(fld, e){
		if( e.getKey() == e.ENTER ){
			var v = fld.getValue();
			var c = this.chkBoxICAO.getValue() == 1 ? 1 : 0;
			this.getStore().load({params: {apt_name: v, icao_only: c}});
		}
	},
	
	get_store: function (){
		if(!this.xStore){
			this.xStore = new Ext.data.JsonStore({
						idProperty: "apt_icao",
						fields: [ 	{name: "flag", type: 'int'},
									{name: "is_icao", type: 'bool'},
									{name: "apt_icao", type: 'string'},
									{name: "apt_name", type: 'string'}
						],
						proxy: new Ext.data.HttpProxy({
							url: "/ajax/airports",
							method: 'GET',
							
						}),
						root: "airports",
						remoteSort: false,
						sortInfo: {field: "apt_icao", direction: 'ASC'}
					});
		}
		return this.xStore;
	}
	
});

// end function cinstructor
