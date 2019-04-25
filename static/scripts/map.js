class Map extends React.Component {
    componentDidMount() {
        var mymapp = L.map('mapp').setView([35.4676, -97.5164], 13);
        L.tileLayer('https://cartodb-basemaps-{s}.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/attribution">CARTO</a>',
            maxZoom: 18,
        }).addTo(mymapp);

        var mapp_markers = getMarkers(mymapp);
        for (var i = 0; i < mapp_markers.length; i++) {
            mapp_markers[i].on("click", function () {
                alert(this.options.address);
            });
        }
    }

    render() {
        return <div id="mapp"></div>
    }
}

ReactDOM.render(<Map/>, document.getElementById('mappy'));

class Address extends React.Component {
    render() {
        return <h1>Hello World</h1>
    }
}

ReactDOM.render(<Address/>, document.getElementById('curaddress'));