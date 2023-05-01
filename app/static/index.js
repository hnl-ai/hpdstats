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

fetch('/api/records')
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
        const { age, ethnicities, sex } = record;

        if (sex === 'M') {
            totalM += 1;
        } else if (sex === 'F') {
            totalF += 1;
        }

        // https://stackoverflow.com/a/175787/6482196
        function isNumeric(str) {
            if (typeof str != "string") return false // we only process strings!  
            return !isNaN(str) && // use type coercion to parse the _entirety_ of the string (`parseFloat` alone does not do this)...
                !isNaN(parseFloat(str)) // ...and ensure strings of whitespace fail
        }

        // Ignore the following as they are probably OCR errors
        if (!isNumeric(age)) continue; // Ignore ages that are not numbers
        if (age.slice(-1) === ".") continue; // Ignore ages that end with a period
        if (parseInt(age) < 18) continue; // Ignore ages under 18

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

const sexChartOptions = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
        }
    }
};

const ageChartOptions = {
    responsive: true,
    scales: {
        x: {
            type: 'linear',
            min: 18,
            suggestedMin: 18,
            // https://www.cnbc.com/2023/02/21/longevity-expert-3-reasons-the-worlds-oldest-person-lived-to-122.html
            max: 122,
            suggestedMax: 122,
        }
    }
};

const ethnicityChartOptions = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        title: {
            display: true,
        }
    }
};

let sexChart = new Chart(
    document.getElementById('sexChart'), {
    type: 'pie',
    data: [],
    options: sexChartOptions,
}
);

let ageChart = new Chart(
    document.getElementById('ageChart'), {
    type: 'scatter',
    data: [],
    options: ageChartOptions,
}
);

let ethnicityChart = new Chart(
    document.getElementById('ethnicityChart'), {
    type: 'polarArea',
    data: [],
    options: ethnicityChartOptions,
}
);

let censusEthnicityChart = new Chart(
    document.getElementById('censusEthnicityChart'), {
    type: 'polarArea',
    data: [],
    options: ethnicityChartOptions,
}
);

let censusSexChart = new Chart(
    document.getElementById('censusSexChart'), {
    type: 'pie',
    data: [],
    options: sexChartOptions,
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
        data: [],
        options: sexChartOptions,
    }
    );

    ageChart = new Chart(
        document.getElementById('ageChart'), {
        type: 'scatter',
        data: [],
        options: ageChartOptions,
    }
    );

    ethnicityChart = new Chart(
        document.getElementById('ethnicityChart'), {
        type: 'polarArea',
        data: [],
        options: ethnicityChartOptions,
    }
    );

    censusSexChart = new Chart(
        document.getElementById('censusSexChart'), {
        type: 'pie',
        data: [],
        options: sexChartOptions,
    }
    );

    censusEthnicityChart = new Chart(
        document.getElementById('censusEthnicityChart'), {
        type: 'polarArea',
        data: [],
        options: ethnicityChartOptions,
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
        const officer = record.arrest_officer[0];
        if (officers[officer]) {
            officers[officer].push(record);
        } else {
            officers[officer] = [record];
        }
    }

    const colorsOfTopArrested = [];

    for (const officer in officers) {
        const matchingRecords = [];
        const arrestedEthnicities = {};
        for (const record of records) {
            if (record.arrest_officer.includes(officer)) {
                matchingRecords.push(record);

                for (const ethnicity of record.ethnicities) {
                    if (arrestedEthnicities[ethnicity]) arrestedEthnicities[ethnicity] += 1;
                    else arrestedEthnicities[ethnicity] = 1
                }
            }
        }

        // https://stackoverflow.com/questions/25500316/sort-a-dictionary-by-value-in-javascript
        const ethnicities = Object.keys(arrestedEthnicities).map(function (key) {
            return [key, arrestedEthnicities[key]];
        });
        ethnicities.sort(function (first, second) {
            return second[1] - first[1];
        });

        if (!ethnicities) continue;
        if (!ethnicities[0]) continue;

        const topArrestedEthnicity = ethnicities[0][0];

        const ethnicityColorMapping = {
            "olive": ["White"],
            // "black": ["Black"], // TODO: Figure out a better color scheme
            "brown": ["Native American", "Hawaiian", "Micronesian", "Samoan", "Tongan", "Hispanic"],
            "yellow": ["Thai", "Chinese", "Filipino", "Indian", "Japanese", "Korean", "Laotian", "Vietnamese", "Other Asian"],
            "black": ["Other", "Unknown"],
        }

        let colorOfTopArrest = 'black';

        for (const color in ethnicityColorMapping) {
            if (ethnicityColorMapping[color].includes(topArrestedEthnicity)) {
                colorOfTopArrest = color;
                break;
            }
        }

        colorsOfTopArrested.push(colorOfTopArrest);
    }

    $('#totalOfficers').text(colorsOfTopArrested.length);
    colorsOfTopArrested.sort();

    for (const colorOfTopArrest of colorsOfTopArrested) {
        const icon = $(`
            <i class="circular user icon ${colorOfTopArrest}"></i>
        `);
        $('#officers').append(icon);
    }
}
