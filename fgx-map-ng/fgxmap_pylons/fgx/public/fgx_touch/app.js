//INITIALIZE ASYNCHRONOUS LOADER
Ext.Loader.setConfig({
    enabled: true,
    paths: {
        ' FGx': '/fgx_touch'
    }
    //, disableCaching: false //FOR DEBUGGING
});
 
Ext.application({
    name: ' FGx',
    requires:[
        ' FGx.model.flight',
        ' FGx.store.flight'
    ],
    controllers: [
        'User'
    ],
    models: [
        'Flight'
    ],
    stores: [
        'Flight'
    ],
    autoCreateViewport: true
});