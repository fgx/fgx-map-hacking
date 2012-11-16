
Ext.ns("FGx");
Ext.define('FGx,MapPanel', {

	extend: 'Ext.Panel',

	constructor: function (name) {
		if (name) {
			this.name = name;
		}
		return this;
	},

	calc: function () {
		alert('base calc');
		return this;
	}
});
			 