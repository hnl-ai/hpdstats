fetch('/data')
  .then((response) => response.json())
  .then((records) => {
    const { allRecords } = records;

    const colHeaders = ['Date', 'Age', 'Sex', 'Ethnicities', 'Arresting Officers', 'Locations', 'Record Image'];
    const data = [];

    for (const record of allRecords) {
      data.push([record.date, record.age, record.sex, record.ethnicities.join(','), record.officers.join(','), record.locations.join(','), `https://honolulupd-records.s3-us-west-1.amazonaws.com/${record.imageId}`])
    }
    $('#recordNum').text(data.length);

    const container = document.getElementById('table');
    const searchField = document.getElementById('search');

    const hot = new Handsontable(container, {
      data,
      rowHeaders: true,
      colHeaders,
      filters: true,
      dropdownMenu: true,
      search: true
    });

    function filter(search) {
      var row, r_len;
      var array = [];
      for (row = 0, r_len = data.length; row < r_len; row++) {
        for (col = 0, c_len = data[row].length; col < c_len; col++) {
          if (('' + data[row][col]).toLowerCase().indexOf(search) > -1) {
            array.push(data[row]);
            break;
          }
        }
      }
      $('#recordNum').text(array.length);
      hot.loadData(array);
    }

    Handsontable.dom.addEvent(searchField, 'keyup', function (event) {
      filter(('' + this.value).toLowerCase());
    });
    $('.ui.sticky')
      .sticky({
        context: '#content'
      })
      ;
  });