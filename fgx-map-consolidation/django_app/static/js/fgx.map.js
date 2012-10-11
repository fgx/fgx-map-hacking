/*!
 * @file fgx.map.js
 *
 *
 */

function FGxMap()
{
	
this.map = null;
        
// wtf is this
document.namespaces;

// @var Graticule Line
this.graticuleLine = new OpenLayers.Symbolizer.Line({
    strokeColor: "#999999",
    strokeDashstyle: "longdash",
    strokeWidth: 0.4
});
            
// @brief Graticule 
this.graticule = new OpenLayers.Control.Graticule({
    numPoints: 2, 
    labelled: true,
    autoActivate: false,
    layerName: "Graticule",
    labelFormat: "dmm",
    lineSymbolizer: this.graticuleLine,
    //visibility:false
});


// @brief Map Options
this.options = { 
    units: 'm',
    // this is the map projection here
    projection: new OpenLayers.Projection("EPSG:3857"),
    //sphericalMercator: true,
    
    // this is the display projection, I need that to show lon/lat in degrees and not in meters
    displayProjection: new OpenLayers.Projection("EPSG:4326"),
    
    // the resolutions are calculated by tilecache, when there is no resolution parameter but a bbox in
    // tilecache.cfg it shows you resolutions for all calculated zoomlevels in your browser: 
    // by http://yoururltothemap.org/tilecache.py/1.0.0/layername/ etc.
    // (This would not be necessary for 4326/900913 because this values are widely spread in
    // openlayer/osm/google threads, you will find the resolutions there)
    resolutions: RESOLUTIONS,
    
    // I set a max and min resolution, means setting available zoomlevels by default
    maxResolution: 156543.03390624999883584678,
    minResolution: 0.29858214169740676658,
    
    // i.e. maxExtent for EPSG 3572 is derived by browsing the very useful map at
    // http://nsidc.org/data/atlas/epsg_3572.html. I tried to get this values with mapnik2 and
    // proj4, but the values I get back with box2d are not very useful at the moment
    maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
    
    // zoomlevels 0-13 = 14 levels ?
    zoomLevels: 20
};


this.init = function () {

    this.mapnik = new OpenLayers.Layer.OSM.Mapnik( "OSM normal" );
    this.mapnik.setOpacity(1.0);

    this.mapnik_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
    this.mapnik_light.setOpacity(0.4);


	this.map = new OpenLayers.Map("map_div", this.options);

	this.map.fractionalZoom = true;

	// Make the layers array to add
	layers_array = [ this.mapnik, this.mapnik_light ]
	layers_array.push.apply(layers_array, LAYERS )
	this.map.addLayers( layers_array );
    

    /*map.events.register('click', map, function (e) {
    OpenLayers.Util.getElement('featureInfo').innerHTML = "Loading... please wait...";
    var url =  wms.getFullRequestString({
                    REQUEST: "GetFeatureInfo",
                    EXCEPTIONS: "application/vnd.ogc.se_inimage",
                    BBOX: wms.map.getExtent().toBBOX(),
                    X: e.xy.x,
                    Y: e.xy.y,
                    FORMAT: 'image/png',
                    INFO_FORMAT: 'text/plain',
                    QUERY_LAYERS: fgx_850_fix.params.LAYERS,
                    WIDTH: wms.map.size.w,
                    HEIGHT: wms.map.size.h
                    });
    xy = e.xy;
    OpenLayers.loadURL(url, false, this, setHTML);
    Event.stop(e);
    });

    function setHTML(response) {
    OpenLayers.Util.getElement('featureInfo').innerHTML = response.responseText
    OpenLayers.Util.getElement('clickInfo').innerHTML = 'Clicked @' + xy + '(long/lat: ' + map.getLonLatFromPixel(xy) + ')'
    }*/
    
    this.map.addControl(this.graticule);
        

    this.map.addControl(new OpenLayers.Control.Permalink('permalink'));
    this.map.addControl(new OpenLayers.Control.MousePosition());
    var ls = new OpenLayers.Control.LayerSwitcher( { roundedCorner: false } );
    this.map.addControl(ls);
    ls.maximizeControl();

    // to get the center point you can disable displayProjection and get the values in
    // meters with the mouse position or permalink
    var centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);
    this.map.setCenter(centerpoint, 5);


} //* init()


}; 
// <<  End FGxMap()