Ext.define('FGx.view.viewport', {
    extend: 'Ext.Panel',
 
    config: {
        fullscreen: true,
        layout: 'card',
        items: [
            {
                xtype: 'flights'
            },
            {
                xtype: 'airports'
            }
        ]
    },
 
    initialize: function() {
        this.setActiveItem(0);
    }
});