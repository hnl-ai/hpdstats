let startDate, endDate;

const start = datepicker('#startDate', { 
    id: 1,
    onSelect: (instance, date) => {
        startDate = date;
        if (startDate && endDate) filterAndRefreshByDate();
    }
});
const end = datepicker('#endDate', {
    id: 1,
    onSelect: (instance, date) => {
        endDate = date;
        if (startDate && endDate) filterAndRefreshByDate();
    }
});

function filterAndRefreshByDate() {
    const records = [];
    for (const record of gAllRecords) {
        const { date } = record;
        if (new Date(date) >= startDate && new Date(date) <= endDate) {
            records.push(record);
        }
    }
    const { 
        totalM,
        totalF,
        ageMapping,
        ethnicityMapping
    } = recount(records);

    repopulateCharts(totalM, totalF, ageMapping, ethnicityMapping);
}

var gAllRecords;

fetch('/data')
    .then((response) => response.json())
    .then((records) => {
        const { allRecords } = records;
        gAllRecords = allRecords;

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

        const { 
            totalM,
            totalF,
            ageMapping,
            ethnicityMapping
        } = recount(allRecords);

        repopulateCharts(totalM, totalF, ageMapping, ethnicityMapping);

        start.setMin(minDate);
        end.setMax(maxDate);
    });

function recount(records) {
    let totalM = totalF = 0;
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

    return {
        totalM,
        totalF,
        ageMapping,
        ethnicityMapping
    }
}

let sexChart = new Chart(
    document.getElementById('sexChart'),
    {
        type: 'pie',
        data: []
    }
);

let ageChart = new Chart(
    document.getElementById('ageChart'),
    {
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
    document.getElementById('ethnicityChart'),
    {
        type: 'polarArea',
        data: []
    }
);

let censusEthnicityChart = new Chart(
    document.getElementById('censusEthnicityChart'),
    {
        type: 'polarArea',
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
    $('#censusEthnicityChart').remove();
    $('#censusEthnicityBreakdown').append('<canvas id="censusEthnicityChart"><canvas>');

    sexChart = new Chart(
        document.getElementById('sexChart'),
        {
            type: 'pie',
            data: []
        }
    );
    
    ageChart = new Chart(
        document.getElementById('ageChart'),
        {
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
        document.getElementById('ethnicityChart'),
        {
            type: 'polarArea',
            data: []
        }
    );
    
    censusEthnicityChart = new Chart(
        document.getElementById('censusEthnicityChart'),
        {
            type: 'polarArea',
            data: []
        }
    );
}

function cleanCharts() {
    ageChart.destroy();
    sexChart.destroy();
    ethnicityChart.destroy();
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
        "Native American/Pacific Islander": ["Native American", "Micronesian", "Samoan", "Tongan"],
        "Asian": ["Chinese", "Filipino", "Indian", "Japanese", "Korean", "Laotian", "Vietnamese"],
        "Hawaiian": ["Hawaiian"],
        "Other": ["Unknown"],
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
    ethnicityChart.data.datasets.push(
        {
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
        }
    );
    ethnicityChart.update();

    censusEthnicityChart.data.labels = Object.keys(ethnicityGroupings);
    censusEthnicityChart.data.datasets.push(
        {
            label: 'Census Dataset (2019)',
            data: [25.5, 2.2, 0.4, 37.6, 10.1, 24.2],
            backgroundColor: [
                'rgb(255, 99, 132)',
                'rgb(75, 192, 192)',
                'rgb(255, 205, 86)',
                'rgb(201, 203, 207)',
                'rgb(54, 162, 235)',
                'rgb(50, 168, 82)'
            ]
        },
    );
    censusEthnicityChart.update();
}