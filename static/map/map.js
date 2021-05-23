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
    let { allRecords } = records;
    allRecords = JSON.parse(allRecords);

    for (const record of allRecords) {
        const location = record.locations[0];
        if (location) {
            const { lat, lng } = location;
            if (lat && lng) {
                const circle = L.circle([lat, lng], {radius: 200}).addTo(map);
                circle.bindPopup(`
                    <div class="ui bulleted list">
                        <div class="item"><b>Age:</b> ${record.age}</div>
                        <div class="item"><b>Ethnicities:</b> ${record.ethnicities.join(', ')}</div>
                        <div class="item"><b>Location:</b> ${record.locations[0].address}</div>
                        <div class="item"><b>Officers:</b> ${record.officers.join(', ')}</div>
                        <div class="item"><a href="https://honolulupd-records.s3-us-west-1.amazonaws.com/${record.imageId}"><b>View Record</b></a></div>
                    </div>
                `);
            }
        }
    }
});