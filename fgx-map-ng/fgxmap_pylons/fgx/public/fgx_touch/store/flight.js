Ext.define('FGx.store.flight', {
    extend: 'Ext.data.Store',
 
    model: 'FGx.model.flight',
    autoLoad: true,
    proxy: {
        type: 'jsonp',
        url: 'http://cf.fgx.ch/data',
        extraParams: {
            'NOT': 'USED'
        },
        callbackKey: 'Xcallback',
        reader: {
            type: 'json',
            root: 'flights'
        }
    }
});
