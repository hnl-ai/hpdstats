const map = L.map('map').setView([21.4389, -158.0001], 11);

L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/light-v10',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoibG92ZW1pbGt0ZWEiLCJhIjoiY2swcGFtb3JzMDhoMDNkcGE5NW9ueGh6aSJ9.OryBJxboTqlp_lmrUyTD1g'
}).addTo(map);

function differenceInDays(d1, d2) { // https://www.geeksforgeeks.org/how-to-calculate-the-number-of-days-between-two-dates-in-javascript/
    const difference = d2.getTime() - d1.getTime();
    return Math.ceil(difference / (1000 * 3600 * 24));
}

const legend = L.control({ position: 'bottomright' });

legend.onAdd = (map) => {

    let div = L.DomUtil.create('div', 'info legend');
    const grades = [0, 3, 7, 30, 180, 365];

    div.innerHTML += '<h3 class="ui header">Days since the arrest</h3>';

    // loop through our density intervals and generate a label with a colored square for each interval
    for (let i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
    }

    return div;
};

legend.addTo(map);

function getColor(d) { // https://colorbrewer2.org/#type=sequential&scheme=Oranges&n=6
    return d > 365 ? '#feedde' :
        d > 180 ? '#fdd0a2' :
        d > 30 ? '#fdae6b' :
        d > 7 ? '#fd8d3c' :
        d > 3 ? '#e6550d' :
        '#a63603';
}

fetch('/api/records')
    .then((response) => response.json())
    .then((records) => {
        const { allRecords } = records;

        for (const record of allRecords) {
            const location = record.locations[0];
            if (location) {
                const { lat, lng } = location;
                if (lat && lng) {
                    const circle = L.circle([lat, lng], {
                        radius: 200,
                        color: getColor(differenceInDays(new Date(record.date), new Date()))
                    });
                    circle.addTo(map);
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