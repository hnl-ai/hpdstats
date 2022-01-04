$(document).ready(() => {
  $('#table').DataTable({
    'processing': true,
    select: true,
    'dom': 'PBfrtip',
    'ajax': {
      'url': '/api/records',
      'dataSrc': 'allRecords'
    },
    'columns': [
      { "data": "date" },
      { "data": "age" },
      { "data": "sex" },
      { "data": "ethnicities" },
      { "data": "arrest_officer" },
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

