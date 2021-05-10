fetch('/data')
  .then((response) => response.json())
  .then((records) => {
    const { allRecords } = records;

    const data = [['Date', 'Age', 'Sex', 'Ethnicities', 'Arresting Officers', 'Locations', 'Record Image']];

    for (const record of allRecords) {
      console.log(record);
      data.push([record.date, record.age, record.sex, record.ethnicities.join(','), record.officers.join(','), record.locations.join(','), `https://honolulupd-records.s3-us-west-1.amazonaws.com/${record.imageId}`])
    }

    const container = document.getElementById('table');
    const hot = new Handsontable(container, {
      data: data,
      rowHeaders: true,
      colHeaders: true,
      filters: true,
      dropdownMenu: true
    });

  });