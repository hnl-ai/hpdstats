# -*- coding: utf-8 -*-
"""The pdfs utility module."""

from PyPDF2 import PdfFileReader, PdfFileWriter

PDF_DIRECTORY = 'pdfs'

def split_into_pages(pdf_file_path):
    """Split a given PDF file into multiple PDF pages."""
    pdf_file = PdfFileReader(pdf_file_path)
    output_pdf_files = []

    for page_num in range(pdf_file.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_file.getPage(page_num))

        file_prefix = pdf_file_path.split('/')[1][0:-4]
        output_filename = f'{PDF_DIRECTORY}/{file_prefix}_page_{page_num + 1}.pdf'

        with open(output_filename, 'wb') as out:
            print(f'Created: {output_filename}')
            pdf_writer.write(out)
            output_pdf_files.append(output_filename)
    return output_pdf_files
