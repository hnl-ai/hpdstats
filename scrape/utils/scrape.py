# -*- coding: utf-8 -*-
"""The scrape utility module."""

import random
from bs4 import BeautifulSoup
import requests

from .s3 import check_if_key_exists, upload_file

USER_AGENTS = [
    (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15'
    ),
    (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) '
        'Gecko/20100101 Firefox/77.0'
    ),
    (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    ),
    (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) '
        'Gecko/20100101 Firefox/77.0'
    ),
    (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    )
]

ARREST_LOG_URL = 'https://www.honolulupd.org/information/arrest-logs/'
PDF_DIRECTORY = 'pdfs'
BUCKET_NAME = 'honolulupd-arrest-logs'

def write_pdf_to_disk(data, key):
    """Writes the given pdf file to the file system."""
    date = ('-'.join(key.split('-')[0:3]))
    output_filename = f'{PDF_DIRECTORY}/{date}.pdf'
    with open(output_filename, 'wb') as output_file:
        output_file.write(data)
    return output_filename

def save_pdf(pdf_link, key):  # Saves the PDF file to S3 and disk
    """Wrapper function to save the given pdf file to the file system and S3."""
    response = requests.get(pdf_link,
        allow_redirects=True,
        headers={'User-Agent': random.choice(USER_AGENTS)}
    )
    upload_file(BUCKET_NAME, key, response.content, 'application/pdf')
    return write_pdf_to_disk(response.content, key)

def check_for_update():
    """Returns a list of local references to new PDF files."""
    response = requests.get(ARREST_LOG_URL,
        headers={'User-Agent': random.choice(USER_AGENTS)}
    )
    soup = BeautifulSoup(response.text, features="html.parser")

    new_pdf_files = []
    for link in soup.find_all('a'):
        pdf_link = link.get('href')
        if pdf_link.endswith('pdf') and "Arrest_Log" in pdf_link:
            key = pdf_link.split('/')[::-1][0]

            if not check_if_key_exists(BUCKET_NAME, key):
                output_filename = save_pdf(pdf_link, key)
                new_pdf_files.append(output_filename)
    return new_pdf_files
