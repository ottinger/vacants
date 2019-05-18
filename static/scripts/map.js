var mymapp = L.map('mappy');
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
    maxZoom: 20,
}).addTo(mymapp);

// Get geojson for cities
if (getCitiesGeoJson()) {
    var citiesGeoJson = getCitiesGeoJson();
    var cities_layer = L.geoJSON(citiesGeoJson, {
        style: {
            color: "#000",
            opacity: 0.05,
            fillColor: "#000",
            fillOpacity: 0.05
        }
    }).addTo(mymapp);
}

// Get geojson for neighborhoods
var neighborhoodsGeoJson = getNeighborhoodsGeoJson();
var neighborhoods_layer = L.geoJSON(neighborhoodsGeoJson, {
    onEachFeature: function (feature, layer) {
        if (feature.properties && feature.properties.name) {
            var popStr = "";
            popStr += feature.properties.name;

            if (feature.properties.pk)
                popStr += "<br><a href=\"" + neighborhoodRoot + feature.properties.pk + "\">More...</a>";
            layer.bindPopup(popStr);

        }
    },
    style: function (feature) {
        return {
            fillColor: "#00F",
            fillOpacity: (feature.properties.property_density / 100) // look at a different method of calculating?
        }
    }
}).addTo(mymapp);

// Get geojson for properties
var mygeojson = getGeoJson();
propertyRadius = 6;
function propertiesStyle() {
    return {
        radius: propertyRadius,
        color: "#FF0000",
        opacity: 1,
        fillOpacity: 0.3
    };
}
var properties_layer = L.geoJSON(mygeojson, {
    onEachFeature: function (feature, layer) {
        if (feature.properties && feature.properties.address) {
            var popStr = "";
            popStr += feature.properties.address;

            if (feature.properties.pk)
                popStr += "<br><a href=\"" + propertyRoot + feature.properties.pk + "\">More...</a>";
            layer.bindPopup(popStr);
        }
    },
    pointToLayer: function (feature, latlng) {
        var theMarker = L.circleMarker(latlng, propertiesStyle());

        return theMarker;
    }
}).addTo(mymapp);

// Set bounds based on either neighborhoods layer or properties layer
if (neighborhoods_layer.getLayers().length > 0)
    mymapp.fitBounds(neighborhoods_layer.getBounds()); // One or more neighborhoods
else
    mymapp.fitBounds(properties_layer.getBounds()); // Individual property

mymapp.on('zoom', function (e) {
    var cz = mymapp.getZoom();
    switch (true) {
        case (cz < 10):
            propertyRadius = 2;
            break;
        case (cz < 13):
            propertyRadius = 3;
            break;
        case (cz < 14):
            propertyRadius = 6;
            break;
        case (cz < 15):
            propertyRadius = 8;
            break;
        case (cz < 16):
            propertyRadius = 10;
            break;
        case (cz < 17):
            propertyRadius = 14;
            break;
        case (cz < 18):
            propertyRadius = 18;
            break;
        case (cz >= 18):
            propertyRadius = 24;
            break;
    }
    console.log("level: " + cz + "\nradius: " + propertyRadius);
    properties_layer.setStyle(propertiesStyle());
});