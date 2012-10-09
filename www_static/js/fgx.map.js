/*!
 * @file fgx.map.js
 *
 *
 */

var map;
        
document.namespaces;

var graticuleLine = new OpenLayers.Symbolizer.Line({
    strokeColor: "#999999",
    strokeDashstyle: "longdash",
    strokeWidth: 0.4
});
            

var graticule = new OpenLayers.Control.Graticule({
    numPoints: 2, 
    labelled: true,
    autoActivate: false,
    layerName: "Graticule",
    labelFormat: "dmm",
    lineSymbolizer: graticuleLine,
    //visibility:false
});


var options = { 
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


function init() {

    
    var mapnik = new OpenLayers.Layer.OSM.Mapnik( "OSM normal" );
    mapnik.setOpacity(1.0);

    var mapnik_light = new OpenLayers.Layer.OSM.Mapnik( "OSM light" );
    mapnik_light.setOpacity(0.4);



    var fgx_ne_landmass = new OpenLayers.Layer.WMS( "NE Landmass", 
        "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
            {
            layers: 'fgx_ne_landmass', 
            format: 'image/png', 
            isBaselayer: true 
            }
        );
    
    
    var fgx_850_apt = new OpenLayers.Layer.WMS( "Airfield", 
        "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
            {layers: 'fgx_850_apt', 
            format: 'image/png',
            transparent:'TRUE'
            },
            {
            visibility:false
            }
        );
    
    var fgx_850_vor = new OpenLayers.Layer.WMS( "VOR", 
        "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
            {layers: 'fgx_850_vor', 
            format: 'image/png',
            transparent:'TRUE'
            },
            {
            visibility:false
            }
        );
    
var fgx_850_dme = new OpenLayers.Layer.WMS( "DME", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?",
        {layers: 'fgx_850_dme', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );
    
var fgx_850_ndb = new OpenLayers.Layer.WMS( "NDB", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
        {layers: 'fgx_850_ndb', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );
    
var fgx_850_ils = new OpenLayers.Layer.WMS( "ILS LOC", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
        {layers: 'fgx_850_ils', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );
    
var fgx_850_ils_info = new OpenLayers.Layer.WMS( "ILS INFO", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
        {layers: 'fgx_850_ils_info', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );
    
var fgx_850_ils_marker = new OpenLayers.Layer.WMS( "ILS OM/MM", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
        {layers: 'fgx_850_ils_marker', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );
    
var fgx_850_fix = new OpenLayers.Layer.WMS( "FIX", 
    "http://map.fgx.ch:81/mapnik/fgxcache.py?", 
        {layers: 'fgx_850_fix', 
        format: 'image/png',
        transparent:'TRUE'
        },
        {
        visibility:false
        }
    );

console.log(options)

map = new OpenLayers.Map("map", options);

map.fractionalZoom = true;

alert("init")

map.addLayers([
    //fgx_ne_landmass,
    mapnik,
    mapnik_light,
    //fgx_850_apt,
    fgx_850_vor,
    fgx_850_dme,
    fgx_850_ndb,
    fgx_850_ils,
    fgx_850_ils_info,
    fgx_850_ils_marker,
    fgx_850_fix
    ]);
    

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
    
    map.addControl(graticule);
        

    map.addControl(new OpenLayers.Control.Permalink('permalink'));
    map.addControl(new OpenLayers.Control.MousePosition());
    var ls = new OpenLayers.Control.LayerSwitcher( { roundedCorner: false } );
    map.addControl(ls);
    ls.maximizeControl();

    // to get the center point you can disable displayProjection and get the values in
    // meters with the mouse position or permalink

    var centerpoint = new OpenLayers.LonLat(939262.20344,5938898.34882);
    map.setCenter(centerpoint,5);


}