const map = L.map('map').setView([21.4389, -158.0001], 11);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibG92ZW1pbGt0ZWEiLCJhIjoiY2swcGFtb3JzMDhoMDNkcGE5NW9ueGh6aSJ9.OryBJxboTqlp_lmrUyTD1g'
}).addTo(map);

fetch('/data')
.then((response) => response.json())
.then((records) => {
    const { allRecords } = records;

    let i = 0;
    for (const record of allRecords) {     
        setTimeout(() => {
            fetch(`https://maps.googleapis.com/maps/api/geocode/json?address=${record.locations[0]}&key=AIzaSyDZGTIy1M5PDaKpInl-jIkflfSdZ4RPm-c`)
            .then((response) => response.json())
            .then((data) => {
                console.log(data);
                if (data.status === "OK") {
                    const { lat, lng } = data.results[0].geometry.location;
                    L.circle([lat, lng], {radius: 200}).addTo(map);
                }
            });
        }, i * 100);   
        i += 1;
    }
});