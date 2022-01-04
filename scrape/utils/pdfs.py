# -*- coding: utf-8 -*-
"""The pdfs utility module."""

from pathlib import Path
from PyPDF2 import PdfFileReader, PdfFileWriter

import constants

def initialize_pdf_directory(pdf_date):
    """Initializes a workspace directory for a given PDF.
        Example Format:
            - 2022-01-01/
                - images/
                - pages/
                - records/
    """
    subdirectories = dict.fromkeys(['images', 'pages', 'records'])

    for subdir_name, _ in subdirectories.items():
        subdir_dir_name = f"{constants.PDF_ROOT_DIRECTORY}/{pdf_date}/{subdir_name}"
        Path(subdir_dir_name).mkdir(parents=True, exist_ok=True)
        subdirectories[subdir_name] = subdir_dir_name

    subdirectories['root'] = f"{constants.PDF_ROOT_DIRECTORY}/{pdf_date}"

    return subdirectories


def split_into_pages(pdf_subdir, pdf_file_path):
    """Split a given PDF file into multiple PDF pages."""
    pdf_file = PdfFileReader(pdf_file_path)
    output_pdf_files = []

    for page_num in range(pdf_file.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_file.getPage(page_num))

        output_filename = f'{pdf_subdir}/{page_num + 1}.pdf'

        with open(output_filename, 'wb') as out:
            print(f'Created: {output_filename}')
            pdf_writer.write(out)
            output_pdf_files.append(output_filename)
    return output_pdf_files
