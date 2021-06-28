from PyPDF2 import PdfFileReader, PdfFileWriter

pdf_directory_location = 'pdfs'


def split_into_pages(pdf_file_path):
    pdf_file = PdfFileReader(pdf_file_path)
    output_pdf_files = []

    for pageNum in range(pdf_file.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf_file.getPage(pageNum))

        output_filename = '{}/{}_page_{}.pdf'.format(pdf_directory_location, pdf_file_path.split('/')[1][0:-4], pageNum + 1)

        with open(output_filename, 'wb') as out:
            print('Created: {}'.format(output_filename))
            pdf_writer.write(out)
            output_pdf_files.append(output_filename)
    return output_pdf_files
