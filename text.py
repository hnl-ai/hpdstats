import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
from PIL import Image
import pytesseract
import string
import re
import boto3

pdf_file_location = 'pdfs/'
image_file_location = 'imgs/'

def add_records(records):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('honolulupd.org-records')
    f = open("current.txt", "r")
    response = table.put_item(
       Item={
            'date': f.read(),
            'records': records
        }
    )

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    png_files = []
    persons = []
    for pageNum in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(pageNum))
        output_filename = '{}_page_{}'.format(fname, pageNum+1)
        with open(pdf_file_location + output_filename + '.pdf', 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(pdf_file_location + output_filename + '.pdf'))
        doc = fitz.open(pdf_file_location + output_filename + '.pdf')
        zoom = 2
        mat = fitz.Matrix(2, 2)
        page = doc.loadPage(0)
        pix = page.getPixmap(matrix=mat)
        output = image_file_location + output_filename
        pix.writePNG(output + '.png')
        im = Image.open(output + '.png')
        width, height = im.size
        if pageNum == 0:
            left = 130
            top = 250
            right = width - 1313
            bottom = height - 40
        else:
            left = 130
            top = 135
            right = width - 1313
            bottom = height - 40
        im1 = im.crop((left, top, right, bottom))
        im1.save(output + '.png')
#        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        ocrstring = pytesseract.image_to_string(Image.open(output + '.png'))
        persons.append(ocrstring.split('\n'))

    results = []
    for arr in persons:
        arr = [re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', x) for x in arr]
        arr = [x for x in arr if x]
        for i, item in enumerate(arr):
            if i % 2 == 0:
                age_and_sex = ''.join(arr[i - 1].split())
                ethnicities = item.split(',')
                res = age_and_sex + ':|:' + item
                print(res)
                results.append(res)
                add_records(results)

path = 'current.pdf'
pdf_splitter(path)
