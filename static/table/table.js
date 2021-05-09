fetch('/data')
  .then((response) => response.json())
  .then((records) => {
    const { allRecords } = records;

    const data = [['Date', 'Age', 'Sex', 'Ethnicities', 'Arresting Officers', 'Locations']];

    for (const record of allRecords) {
      data.push([record.date, record.age, record.sex, record.ethnicities.join(','), record.officers.join(','), record.locations.join(',')])
    }

    const container = document.getElementById('table');
    const hot = new Handsontable(container, {
      data: data,
      rowHeaders: true,
      colHeaders: true,
      filters: true,
      dropdownMenu: true
    });

    //   let totalM = totalF = 0;
    //   const ageMapping = {};
    //   const ethnicityMapping = {};

    //   for (const recordset of allRecords) {
    //     const { date, records } = recordset;

    //     for (const record of records) {
    //       const [ sexAndAge, ethnicities ] = record.split(':|:');
    //       const [ sex, age ] = sexAndAge.split('/');
    //       if (sex === 'M') {
    //         totalM += 1;
    //       } else if (sex === 'F')  {
    //         totalF += 1;
    //       }

    //       if (!ageMapping[age]) {
    //         ageMapping[age] = 1;
    //       } else {
    //         ageMapping[age] += 1;
    //       }

    //       for (const ethnicity of ethnicities.split(',')) {
    //         if (!ethnicityMapping[ethnicity.trim()]) {
    //           ethnicityMapping[ethnicity.trim()] = 1;
    //         } else {
    //           ethnicityMapping[ethnicity.trim()] += 1;
    //         }
    //       }
    //     }
    //   }

    //   const sexData = {
    //     labels: [
    //       'M', "F"
    //     ],
    //     datasets: [{
    //       label: 'Sex Dataset',
    //       data: [totalM, totalF],
    //       backgroundColor: [
    //         'rgb(54, 162, 235)',
    //         'rgb(255, 99, 132)'
    //       ],
    //       hoverOffset: 4
    //     }],
    //   };

    //   const sexChart = new Chart(
    //     document.getElementById('sexChart'),
    //     {
    //       type: 'pie',
    //       data: sexData
    //     }
    //   );

    //   const ageArr = [];
    //   for (const age in ageMapping) {
    //     ageArr.push({
    //       x: age,
    //       y: ageMapping[age]
    //     });
    //   }

    //   const ageData = {
    //     datasets: [{
    //       label: 'Age Dataset',
    //       data: ageArr,
    //       backgroundColor: 'rgb(255, 99, 132)'
    //     }]
    //   };

    //   const ageChart = new Chart(
    //     document.getElementById('ageChart'),
    //     {
    //       type: 'scatter',
    //       data: ageData,
    //       options: {
    //         scales: {
    //           x: {
    //             type: 'linear',
    //             position: 'bottom'
    //           }
    //         }
    //       }
    //     }
    //   );

    //   const ethnicityGroupings = {
    //     "White": ["White"],
    //     "Black": ["Black"],
    //     "Native American/Pacific Islander": ["Native American", "Micronesian", "Samoan", "Tongan"],
    //     "Asian": ["Chinese", "Filipino", "Indian", "Japanese", "Korean", "Laotian", "Vietnamese"],
    //     "Hawaiian": ["Hawaiian"],
    //     "Other": ["Unknown"],
    //   }

    //   const ethnicityArr = new Array(Object.keys(ethnicityGroupings).length).fill(0);
    //   for (const ethnicity of Object.keys(ethnicityMapping)) {
    //     for (const groupingIdx in Object.keys(ethnicityGroupings)) {
    //       const grouping = Object.keys(ethnicityGroupings)[groupingIdx];
    //       if (ethnicityGroupings[grouping].includes(ethnicity)) {
    //         ethnicityArr[groupingIdx] += ethnicityMapping[ethnicity];
    //       }
    //     }
    //   }

    //   const ethnicityData = {
    //     labels: Object.keys(ethnicityGroupings),
    //     datasets: [
    //     {
    //       label: 'Ethniciy Dataset',
    //       data: ethnicityArr,
    //       backgroundColor: [
    //         'rgb(255, 99, 132)',
    //         'rgb(75, 192, 192)',
    //         'rgb(255, 205, 86)',
    //         'rgb(201, 203, 207)',
    //         'rgb(54, 162, 235)',
    //         'rgb(50, 168, 82)'
    //       ]
    //     }
    //   ]
    // };

    //   const ethnicityChart = new Chart(
    //     document.getElementById('ethnicityChart'),
    //     {
    //       type: 'polarArea',
    //       data: ethnicityData
    //     }
    //   );

    //   const censusEthnicityData = {
    //     labels: Object.keys(ethnicityGroupings),
    //     datasets: [
    //       {
    //         label: 'Census Dataset (2019)',
    //         data: [25.5, 2.2, 0.4, 37.6, 10.1, 24.2],
    //         backgroundColor: [
    //           'rgb(255, 99, 132)',
    //           'rgb(75, 192, 192)',
    //           'rgb(255, 205, 86)',
    //           'rgb(201, 203, 207)',
    //           'rgb(54, 162, 235)',
    //           'rgb(50, 168, 82)'
    //         ]
    //       },
    //     ]
    //   };

    //   const censusEthnicityChart = new Chart(
    //     document.getElementById('censusEthnicityChart'),
    //     {
    //       type: 'polarArea',
    //       data: censusEthnicityData
    //     }
    //   );

  });