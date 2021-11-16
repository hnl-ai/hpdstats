$('.ui.sticky')
    .sticky({
        context: '#content',
        pushing: true
    });

let startDate, endDate;

const start = datepicker('#startDate', {
    id: 1,
    onSelect: (instance, date) => {
        startDate = date;
        if (startDate && endDate) filterAndRefreshByDate();
    }
});
start.setDate(new Date(2021, 03, 07)); // April 7th, 2021; First Day I started collecting this information

const end = datepicker('#endDate', {
    id: 1,
    onSelect: (instance, date) => {
        endDate = date;
        if (startDate && endDate) filterAndRefreshByDate();
    }
});

function filterAndRefreshByDate() {
    setNumDays(Math.round(Math.abs((endDate - startDate) / (24 * 60 * 60 * 1000))) + 1);

    const records = [];
    for (const record of gAllRecords) {
        const { date } = record;
        const d = new Date(date);
        d.setHours(0);

        if (d >= startDate && d <= endDate) {
            records.push(record);
        }
    }
    const {
        totalM,
        totalF,
        ageMapping,
        ethnicityMapping
    } = recount(records);

    fillOfficerData(records);
    setMaleFemaleRatio(totalF, totalM);
    repopulateCharts(totalM, totalF, ageMapping, ethnicityMapping);
}

var gAllRecords;

fetch('/data')
    .then((response) => response.json())
    .then((records) => {
        const { allRecords } = records;

        gAllRecords = allRecords;

        fillOfficerData(allRecords);

        let minDate;
        let maxDate;

        for (const record of allRecords) {
            const { age, courts, date, ethnicities, id, imageId, locations, officers, sex } = record;
            if (!minDate || !maxDate) {
                minDate = maxDate = new Date(date);
            } else if (minDate > new Date(date)) {
                minDate = new Date(date);
            } else if (maxDate < new Date(date)) {
                maxDate = new Date(date);
            }
        }
        start.setMin(minDate);
        startDate = minDate;

        end.setMax(maxDate);
        end.setDate(maxDate);
        endDate = maxDate;

        setNumDays(Math.round(Math.abs((maxDate - minDate) / (24 * 60 * 60 * 1000))));
        maxDate.setDate(maxDate.getDate() + 1);
        $('#dataLastUpdatedDate').text(maxDate.toLocaleDateString("en-US"));

        const {
            totalM,
            totalF,
            ageMapping,
            ethnicityMapping
        } = recount(allRecords);

        setMaleFemaleRatio(totalF, totalM);
        repopulateCharts(totalM, totalF, ageMapping, ethnicityMapping);
    });

function setMaleFemaleRatio(totalF, totalM) {
    const mToFRatio = totalM / totalF;
    $('#maleFemaleRatio').text(`~${Math.floor(mToFRatio * 100)} M:100 F`);
}

function setNumRecords(num) {
    $('#numRecords').text(`${num}`);
}

function setNumDays(num) {
    $('#numDays').text(`${num}`);
}

function setAgeStats(ageMapping) {
    const numbers = [];
    for (const age in ageMapping) {
        if (!isNaN(age)) {
            numbers.push(...new Array(ageMapping[age]).fill(Number(age)));
        }
    }

    const mode = Object.keys(ageMapping).reduce((a, b) => ageMapping[a] > ageMapping[b] ? a : b);
    const mean = (numbers) => Math.round(numbers.reduce((acc, val) => acc + val, 0) / numbers.length);
    let median = 0;
    numbers.sort();

    if (numbers.length % 2 === 0) {
        median = (numbers[numbers.length / 2 - 1] + numbers[numbers.length / 2]) / 2;
    } else {
        median = numbers[(numbers.length - 1) / 2];
    }
    $('#ageMean').text(mean(numbers));
    $('#ageMode').text(mode);
    $('#ageMedian').text(median);

}

function recount(records) {
    setNumRecords(records.length);

    let totalM = 0;
    let totalF = 0;
    const ageMapping = {};
    const ethnicityMapping = {};

    for (const record of records) {
        const { age, courts, date, ethnicities, id, imageId, locations, officers, sex } = record;

        if (sex === 'M') {
            totalM += 1;
        } else if (sex === 'F') {
            totalF += 1;
        }

        if (!ageMapping[age]) {
            ageMapping[age] = 1;
        } else {
            ageMapping[age] += 1;
        }

        for (const ethnicity of ethnicities) {
            if (!ethnicityMapping[ethnicity.trim()]) {
                ethnicityMapping[ethnicity.trim()] = 1;
            } else {
                ethnicityMapping[ethnicity.trim()] += 1;
            }
        }
    }

    setAgeStats(ageMapping);

    return {
        totalM,
        totalF,
        ageMapping,
        ethnicityMapping
    }
}

let sexChart = new Chart(
    document.getElementById('sexChart'), {
    type: 'pie',
    data: []
}
);

let ageChart = new Chart(
    document.getElementById('ageChart'), {
    type: 'scatter',
    data: [],
    options: {
        scales: {
            x: {
                type: 'linear',
                position: 'bottom'
            }
        }
    }
}
);

let ethnicityChart = new Chart(
    document.getElementById('ethnicityChart'), {
    type: 'polarArea',
    data: []
}
);

let censusEthnicityChart = new Chart(
    document.getElementById('censusEthnicityChart'), {
    type: 'polarArea',
    data: []
}
);

let censusSexChart = new Chart(
    document.getElementById('censusSexChart'), {
    type: 'pie',
    data: []
}
);

function initializeCharts() {
    $('#sexChart').remove();
    $('#sexBreakdown').append('<canvas id="sexChart"><canvas>');
    $('#ageChart').remove();
    $('#ageBreakdown').append('<canvas id="ageChart"><canvas>');
    $('#ethnicityChart').remove();
    $('#ethnicityBreakdown').append('<canvas id="ethnicityChart"><canvas>');

    $('#censusSexChart').remove();
    $('#censusSexBreakdown').append('<canvas id="censusSexChart"></canvas>');
    $('#censusEthnicityChart').remove();
    $('#censusEthnicityBreakdown').append('<canvas id="censusEthnicityChart"><canvas>');

    sexChart = new Chart(
        document.getElementById('sexChart'), {
        type: 'pie',
        data: []
    }
    );

    ageChart = new Chart(
        document.getElementById('ageChart'), {
        type: 'scatter',
        data: [],
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    }
    );

    ethnicityChart = new Chart(
        document.getElementById('ethnicityChart'), {
        type: 'polarArea',
        data: []
    }
    );

    censusSexChart = new Chart(
        document.getElementById('censusSexChart'), {
        type: 'pie',
        data: []
    }
    );

    censusEthnicityChart = new Chart(
        document.getElementById('censusEthnicityChart'), {
        type: 'polarArea',
        data: []
    }
    );
}

function cleanCharts() {
    ageChart.destroy();
    sexChart.destroy();
    ethnicityChart.destroy();
    censusSexChart.destroy();
    censusEthnicityChart.destroy();
    initializeCharts();
}

function repopulateCharts(totalM, totalF, ageMapping, ethnicityMapping) {
    cleanCharts();

    sexChart.data.labels = ['M', 'F'];
    sexChart.data.datasets.push({
        label: 'Sex Dataset',
        data: [totalM, totalF],
        backgroundColor: [
            'rgb(54, 162, 235)',
            'rgb(255, 99, 132)'
        ],
        hoverOffset: 4
    });
    sexChart.update();

    const ageArr = [];
    for (const age in ageMapping) {
        ageArr.push({
            x: age,
            y: ageMapping[age]
        });
    }

    ageChart.data.datasets.push({
        label: 'Age Dataset',
        data: ageArr,
        backgroundColor: 'rgb(255, 99, 132)'
    });
    ageChart.update();

    const ethnicityGroupings = {
        "White": ["White"],
        "Black": ["Black"],
        "Native American": ["Native American"],
        "Asian": ["Thai", "Chinese", "Filipino", "Indian", "Japanese", "Korean", "Laotian", "Vietnamese"],
        "Hawaiian/Pacific Islander": ["Hawaiian", "Micronesian", "Samoan", "Tongan"],
        "Other": ["Other", "Other Asian", "Unknown", "Hispanic"],
    }

    const ethnicityArr = new Array(Object.keys(ethnicityGroupings).length).fill(0);
    for (const ethnicity of Object.keys(ethnicityMapping)) {
        for (const groupingIdx in Object.keys(ethnicityGroupings)) {
            const grouping = Object.keys(ethnicityGroupings)[groupingIdx];
            if (ethnicityGroupings[grouping].includes(ethnicity)) {
                ethnicityArr[groupingIdx] += ethnicityMapping[ethnicity];
            }
        }
    }

    ethnicityChart.data.labels = Object.keys(ethnicityGroupings);
    ethnicityChart.data.datasets.push({
        label: 'Ethniciy Dataset',
        data: ethnicityArr,
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(255, 205, 86)',
            'rgb(201, 203, 207)',
            'rgb(54, 162, 235)',
            'rgb(50, 168, 82)'
        ]
    });

    const sum = ethnicityArr.reduce((a, b) => a + b, 0);
    ethnicityChart.update();

    $('#whiteRatio').text(`${Math.round(((ethnicityArr[0] / sum) * 100))}%`);
    $('#blackRatio').text(`${Math.round(((ethnicityArr[1] / sum) * 100))}%`);
    $('#nativeAmericanRatio').text(`${Math.round(((ethnicityArr[2] / sum) * 100))}%`);
    $('#asianRatio').text(`${Math.round(((ethnicityArr[3] / sum) * 100))}%`);
    $('#hawaiianRatio').text(`${Math.round(((ethnicityArr[4] / sum) * 100))}%`);

    censusSexChart.data.labels = ['M', 'F'];
    censusSexChart.data.datasets.push({
        label: 'Census Sex Dataset (2019)',
        data: [503609, 488179],
        backgroundColor: [
            'rgb(54, 162, 235)',
            'rgb(255, 99, 132)'
        ],
        hoverOffset: 4
    });
    censusSexChart.update();

    censusEthnicityChart.data.labels = Object.keys(ethnicityGroupings);
    censusEthnicityChart.data.datasets.push({
        label: 'Census Ethnicity Dataset (2019)',
        data: [25.5, 2.2, 0.4, 37.6, 10.1, 24.2],
        backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(75, 192, 192)',
            'rgb(255, 205, 86)',
            'rgb(201, 203, 207)',
            'rgb(54, 162, 235)',
            'rgb(50, 168, 82)'
        ]
    });
    censusEthnicityChart.update();
}

function fillOfficerData(records) {
    $('#officers').empty();
    const officers = {};

    for (const record of records) {
        const officer = record.officers[0];
        if (officers[officer]) {
            officers[officer].push(record);
        } else {
            officers[officer] = [record];
        }
    }

    $('#totalOfficers').text(Object.keys(officers).length);

    let i = 0;
    for (const officer in officers) {
        const matchingRecords = [];
        const arrestedEthnicities = {};
        for (const record of records) {
            if (record.officers.includes(officer)) {
                matchingRecords.push(record);
    
                for (const ethnicity of record.ethnicities) {
                    if (arrestedEthnicities[ethnicity]) arrestedEthnicities[ethnicity] += 1;
                    else arrestedEthnicities[ethnicity] = 1
                }
            }
        }
    
        // https://stackoverflow.com/questions/25500316/sort-a-dictionary-by-value-in-javascript
        const ethnicities = Object.keys(arrestedEthnicities).map(function(key) {
            return [key, arrestedEthnicities[key]];
        });
        ethnicities.sort(function(first, second) {
            return second[1] - first[1];
        });
    
        const officerList = [];
        for (const ethnicity of ethnicities.slice(0, 3)) { // Top 3 arrested
            officerList.push(
                `<div class='item'>${ethnicity[1]} ${ethnicity[1] > 1 ? 'were' : 'was'} ${ethnicity[0]}</div>`
            );
        }

        const popup =
            `<div id="officer-${i}-popup" class="ui flowing popup top center transition hidden">
                <p style="text-align: center">Total Arrests: ${matchingRecords.length}</p>
                <div class="ui one column divided center aligned grid">
                    <div class="column">
                        <h4 class="ui header">Top 3 Ethnicities Arrested</h4>
                        <div class="ui bulleted list">
                            ${officerList.join('\n')}
                        </div>
                    </div>
                </div>
            </div>
        `;

        const icon = $(`
            <i id="officer-${i}-icon" class="circular user icon"></i>
            ${popup}
        `);
        $('#officers').append(icon);
        $(`#officer-${i}-icon`)
            .popup({
                inline: `officer-${i}-popup`
            });

        i += 1;
    }
}
