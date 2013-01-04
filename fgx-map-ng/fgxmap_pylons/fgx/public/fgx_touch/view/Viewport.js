Ext.define('FGx.view.Viewport', {
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