Ext.define('FGx.store.Flight', {
    extend: 'Ext.data.Store',
 
    model: 'FGx.model.Flight',
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
