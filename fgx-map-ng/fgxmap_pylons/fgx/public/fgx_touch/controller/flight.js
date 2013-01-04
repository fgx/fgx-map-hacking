Ext.define('FGx.controller.flight', {
    extend: 'Ext.app.Controller',
 
    //REGISTER CLASSES
    requires:[
        'MyApp.ui.LoginForm'
    ],
 
    //REGISTER MVC
    models: [
        'flight'
    ],
    stores: [
        'flight'
    ],
    views: [
        'flight.List',
        'flight.Detail'
    ],
 
    init: function() {
        this.control({
            //SUBSCRIBE TO EVENTS
            '.userlist #lstUser': {
                itemtap: this.onUserItemTap
            },
            '.userlist #btnSettings': {
                tap: this.onSettingsTap
            }
        });
    },
 
    //ACTIONS
    detail: function(options) {
        //UPDATE STORE WITH USER INFO
        var user = Ext.ComponentQuery.query('.userdetail #lstDetail')[0];
        user.getStore().getProxy().extraParams.UserID = options.Id;
        user.getStore().read();
 
        //SELECT USER INFO VIEW
        Ext.Viewport.getActiveItem().setActiveItem(1);
    },
 
    //EVENTS
    onUserItemTap: function (dataView, index) {
        var item = dataView.getStore().getAt(index);
        this.detail(item.data);
    },
 
    onSettingsTap: function() {
        var popup = Ext.create('MyApp.ui.LoginForm');
        Ext.Viewport.add(popup);
    }
});