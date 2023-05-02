fetch('https://raw.githubusercontent.com/hnl-ai/hpdstats/main/active-police-dispatch-calls/current.txt')
.then(response => response.text())
.then((data) => {
    const lines = data.split('\n');
    const date = lines[0];
    const dispatches = lines.slice(1, lines.length - 1);

    $('#activeDispatchesDateTime').text(new Date(date).toLocaleString('en-US', { timeZone: 'Pacific/Honolulu' }));

    dispatches.forEach((dispatch) => {
        let [time, type, address, city, _] = dispatch.split('|');
        time = time.split('   ')[1];

        $('#activeDispatchesTableBody').append(
            `<tr>
                <td>${time}</td>
                <td>${type}</td>
                <td>${address}</td>
                <td>${city}</td>
            </tr>`
        );
    });
});

$(document).ready(() => {
    $('table').tablesort()
});
