$(document).ready(() => {
  $('#table').DataTable({
    'processing': true,
    select: true,
    'dom': 'PBfrtip',
    'ajax': {
      'url': '/data',
      'dataSrc': 'allRecords'
    },
    'columns': [
      { "data": "date" },
      { "data": "age" },
      { "data": "sex" },
      { "data": "ethnicities" },
      { "data": "officers" },
      {
        "data": (row, type, val, meta) => {
          return row.locations.length ? row.locations[0].address : "";
        }
      },
      //TODO: link to image with imageId field?
    ],
    'buttons': [
      'excel', 'colvis'
    ],
    'fixedHeader': true
  });
});

