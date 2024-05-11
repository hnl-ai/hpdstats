fetch('/api/archives')
    .then((response) => response.json())
    .then((data) => {
        const { archives } = data;

        const monthYears = {}; // Month/Year pairing

        for (const archive of archives) {
            const [yy, mm, dd] = archive.split('-').slice(0, 3);
            const date = new Date(yy, mm - 1, dd);
            
            // Don't render any non-date files
            // This includes files like robots.txt
            if (isNaN(date.getTime())) {
                continue;
            }

            const month = date.toLocaleString('default', { month: 'long' });
            const year = date.getFullYear();
            const key = `${month}_${year}`;

            if (!monthYears[key]) {
                monthYears[key] = [archive];
            } else {
                monthYears[key].push(archive);
            }
        }

        for (const [monthYear, records] of Object.entries(monthYears).reverse()) {
            const [month, year] = monthYear.split('_');
            $('#archiveList')
                .append($(`
            <div class="title">
                <i class="dropdown icon"></i> ${month} ${year}
            </div>
            <div class="content">
            ${records.map((e) => {
                    return `
                    <p>
                        <i class="large folder middle aligned icon"></i>
                        <a class="header" href="https://honolulupd-arrest-logs.s3-us-west-1.amazonaws.com/${e}">${e}</a>

                    </p>
                `;
                }).join('\n')}
            </div>
        `));
        }
        $('.ui.accordion').accordion();
    });