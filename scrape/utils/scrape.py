# -*- coding: utf-8 -*-
"""The scrape utility module."""

import random
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

import constants
from .s3 import check_if_key_exists, upload_file

ua = UserAgent()

def write_pdf_to_disk(data, key):
    """Writes the given pdf file to the file system."""
    # Example Date: "2022-01-01"
    date = key[:10]
    output_filename = f'{constants.PDF_ROOT_DIRECTORY}/{date}.pdf'
    with open(output_filename, 'wb') as output_file:
        output_file.write(data)
    return output_filename


def save_pdf(pdf_link, key):  # Saves the PDF file to S3 and disk
    """Wrapper function to save the given pdf file to the file system and S3."""
    response = requests.get(pdf_link,
                            allow_redirects=True,
                            headers={'User-Agent': ua.random}
                            )
    response.raise_for_status()
    upload_file(
        constants.LOGS_BUCKET_NAME,
        key,
        response.content,
        'application/pdf')
    return write_pdf_to_disk(response.content, key)


def check_for_update():
    """Returns a list of local references to new PDF files."""
    response = requests.get(constants.ARREST_LOG_URL,
                            headers={'User-Agent': ua.random}
                            )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features="html.parser")

    new_pdf_files = []
    for link in soup.find_all('a'):
        # Example HREF
        # "https://www.honolulupd.org/wp-content/hpd/arrest-logs/2022-01-01-12-00-26_Arrest_Log.pdf"
        href = link.get('href')
        if not href.endswith('pdf'):  # Skip Non-PDF files
            continue

        if "Arrest_Log" not in href:  # Skip Non-Arrest Log Files
            continue

        # Example KEY "2022-01-01-12-00-26_Arrest_Log.pdf"
        key = href.split('/')[::-1][0]

        if not check_if_key_exists(constants.LOGS_BUCKET_NAME, key):
            output_filename = save_pdf(href, key)
            new_pdf_files.append(output_filename)
    return new_pdf_files
