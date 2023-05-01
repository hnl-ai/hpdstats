import requests
from bs4 import BeautifulSoup
import random
import re
from datetime import datetime
import os.path
import json

USER_AGENTS = [
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
     'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) '
     'Gecko/20100101 Firefox/77.0'),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) '
     'Gecko/20100101 Firefox/77.0'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36')]

url = 'https://www.honolulupd.org/wp-content/hpd/cfs/Incidents_past_24_hours.html'

r = requests.get(url, allow_redirects=True,
    headers={
        'User-Agent': random.choice(USER_AGENTS)
    }
)

soup = BeautifulSoup(r.text, 'html.parser')

last_updated_regex = re.compile(r'Data last updated on')

last_updated = soup.find(text=last_updated_regex).next_element.text # Example: December 13, 2022 22:14:00 PM

last_updated_date = datetime.strptime(last_updated, "%B %d, %Y %H:%M:%S %p").isoformat() # Example: 2022-12-13T22:29:04

output_file_name = 'archive/' + last_updated_date + '.txt'

if (os.path.isfile(output_file_name)): # If we already have a file for this date, don't proceed
    print(f"File already exists for {last_updated_date} date. Exiting.")
    exit(0)

oReport = soup.find('td', { 'id': 'oReportCell' })

rows = oReport.findAll('tr', {"valign" : "top"})

with open('current.txt', 'w') as out:
    out.write(last_updated_date + '\n')
    for row in rows[3:]:
        text = row.getText(separator=u'|')
        out.write(text + '\n')

with open(output_file_name, 'w') as out:
    for row in rows[3:]:
        text = row.getText(separator=u'|')
        out.write(text + '\n')

with open('info.json', 'r') as infile:
    json_object = json.load(infile)
    for row in rows[3:]:
        row_data = row.getText(separator=u'|').split('|')
        incident = row_data[1]
        city = row_data[3]
        district = row_data[4]

        if incident not in json_object['incidentCount']:
            json_object['incidentCount'][incident] = 0
        json_object['incidentCount'][incident] += 1

        if city not in json_object['cityCount']:
            json_object['cityCount'][city] = 0
        json_object['cityCount'][city] += 1

        if district not in json_object['districtCount']:
            json_object['districtCount'][district] = 0
        json_object['districtCount'][district] += 1
    with open("info.json", "w") as outfile:
        json.dump(json_object, outfile, indent = 2)
