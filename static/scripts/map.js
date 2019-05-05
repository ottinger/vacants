var mymapp = L.map('mappy').setView([35.4676, -97.5164], 13);
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
    maxZoom: 18,
}).addTo(mymapp);

// Get geojson for neighborhoods
var neighborhoodsGeoJson = getNeighborhoodsGeoJson();
L.geoJSON(neighborhoodsGeoJson, {
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
L.geoJSON(mygeojson, {
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
        return L.circleMarker(latlng, {
            radius: 6,
            color: "#FF0000",
            opacity: 1,
            fillOpacity: 0.3
        })
    }
}).addTo(mymapp);