Ext.define('FGx.model.flight', {
    extend: 'Ext.data.Model',
     
    fields: [
        'fid',
        'callsign',
        'lat',
        'lon',
        'alt_ft',
		'spd_kt',
		'hdg',
        'model'
    ]
});