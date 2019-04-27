var mymapp = L.map('mappy').setView([35.4676, -97.5164], 13);
L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
    maxZoom: 18,
}).addTo(mymapp);

var mygeojson = getGeoJson();
console.log(mygeojson);
L.geoJSON(mygeojson).addTo(mymapp);

var neighborhoodsGeoJson = getNeighborhoodsGeoJson();
L.geoJSON(neighborhoodsGeoJson).addTo(mymapp);