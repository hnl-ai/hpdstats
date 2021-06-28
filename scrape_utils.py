import random

from s3_utils import check_if_key_exists, upload_file

from bs4 import BeautifulSoup
import requests

user_agent_list = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]
url = 'https://www.honolulupd.org/information/arrest-logs/'
pdf_directory_location = 'pdfs'
bucket_name = 'honolulupd-arrest-logs'


def write_pdf_to_disk(data, key):
    date = ('-'.join(key.split('-')[0:3]))
    output_filename = '{}/{}.pdf'.format(pdf_directory_location, date)
    open(output_filename, 'wb').write(data)
    return output_filename


def save_pdf(pdf_link, key):  # Saves the PDF file to S3 and disk
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    r = requests.get(pdf_link, allow_redirects=True, headers=headers)

    upload_file(bucket_name, key, r.content, 'application/pdf')
    return write_pdf_to_disk(r.content, key)


def check_for_update():  # Returns a list of local references to new PDF files
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, features="html.parser")

    new_pdf_files = []
    for link in soup.find_all('a'):
        pdf_link = link.get('href')
        if pdf_link.endswith('pdf') and "Arrest_Log" in pdf_link:
            key = pdf_link.split('/')[::-1][0]

            if not check_if_key_exists(bucket_name, key):
                output_filename = save_pdf(pdf_link, key)
                new_pdf_files.append(output_filename)
    return new_pdf_files

