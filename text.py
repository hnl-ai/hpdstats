import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import fitz
from PIL import Image
import pytesseract
import string
import re
import boto3
from operator import itemgetter
import cv2
import uuid
import sys

pdf_file_location = 'pdfs/'
image_file_location = 'imgs/'

def getDimensions(field, height, width):
    dimensions = {
        'race_age_and_sex': {
            'left': 130,
            'right': width - 1313
        },
        'location_officer_and_court': {
            'left': 830,
            'right': width - 320            
        }
    }
    return dimensions[field]

def upload_file(path, fileid):
    s3 = boto3.client('s3')
    with open(path, "rb") as f:
        s3.upload_fileobj(f, 'honolulupd-records', fileid,
            ExtraArgs={
                'ACL': 'public-read',
                'ContentType': 'image/png'
            }
        )

def add_record(record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('honolulupd.org-records')
    response = table.put_item(
       Item={
            'date': sys.argv[1],
            **record
        }
    )

def imageCrop(path, dimension):
    im = Image.open(path)
    width, height = im.size
    dimensions = getDimensions(dimension, height, width)
    left, right = itemgetter('left', 'right')(dimensions)
    im1 = im.crop((left, 0, right, height))
    output_file_name = path[0:-4] + dimension + '.png'
    im1.save(output_file_name)
    return output_file_name

def readText(path):
    ocrstring = pytesseract.image_to_string(Image.open(path))
    return ocrstring

def handle_race_age_and_sex(text):
    race_age_and_sex_output = [text.split('\n')]
    for arr in race_age_and_sex_output:
        arr = [re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', x) for x in arr]
        arr = [x for x in arr if x]
        for i, item in enumerate(arr):
            if i % 2 == 1:                
                if (len(item.split('/'))) == 2:
                    [sex, age] = item.split('/')
                else:
                    sex = item[0]
                    age = item[-3:-1]
                ethnicities = arr[i - 1].split(',')
                ethnicities = clean_ethnicities(ethnicities)
                
                return (age, sex, ethnicities)
                

def handle_location_officer_and_court(text):
    location_officer_and_court_output = [text.split('\n\n')]
    result = {
        'locations': [],
        'officers': [],
        'courts': []
    }
    for arr in location_officer_and_court_output:
        arr = [re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', x) for x in arr]
        for i, item in enumerate(arr):
            item = item.split('\n')
            item = [x for x in item if x]
            if (len(item) == 1):
                continue
            while(len(item) < 3):
                item.append('')
            [location, officer, court] = item
            result['locations'].append(location)
            result['officers'].append(officer)
            result['courts'].append(court)
    return (
        result['locations'],
        result['officers'],
        result['courts']
    )

def clean_ethnicities(ethnicities):
    ethnicities = list(filter(None, ethnicities))
    ethnicities = [x.strip() for x in ethnicities]
    # Rudimentary OCR corrections
    errors = {
        "Filipino": ["Filipi", "Filipir"],
        "Hawaiian": ["Hawe", "Haw:", "Hawai", "Hawaiia", "Hawaiie", "Hav"],
        "Samoan": ["Sar", "Samoar", "Samoi", "Sarr"],
        "Hispanic": ["Hispani"],
        "Other": ["Othe", "Othe:", "Other Pac. Isl", "Other Pac. Isl:", "Other P"],
        "Unknown": ["H", "C", "Unkr"],
        "Indian": ["India"],
        "Japanese": ["Japane:", "Japan", "Japai"],
        "Native American": ["Native Americ"],
        "Chinese": ["Chin"],
        "Tongan":  ["Ton", "Tong"],
        "Micronesian": ["Micr"],
        "Laotian": ["Laotia"]
    }
    cleaned_ethnicities = []

    for x in ethnicities:
        inserted = False
        for y in errors:
            if x in errors[y]:
                cleaned_ethnicities.append(y)
                inserted = True
        if not inserted:
            cleaned_ethnicities.append(x)

    return cleaned_ethnicities

def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    png_files = []
    for pageNum in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(pageNum))
        output_filename = '{}_page_{}'.format(fname, pageNum+1)
        with open(pdf_file_location + output_filename + '.pdf', 'wb') as out:
            pdf_writer.write(out)
        print('Created: {}'.format(pdf_file_location + output_filename + '.pdf'))
        doc = fitz.open(pdf_file_location + output_filename + '.pdf')
        mat = fitz.Matrix(2, 2)
        page = doc.loadPage(0)
        pix = page.getPixmap(matrix=mat)
        pix.writePNG(image_file_location + output_filename + '.png')
        png_files.append(image_file_location + output_filename + '.png')
    for i, pngFile in enumerate(png_files):
        im = Image.open(pngFile)
        width, height = im.size
        if i == 0:
            left = 0
            top = 270
            right = width
            bottom = height - 100
        else:
            left = 0
            top = 160
            right = width
            bottom = height - 90
        im1 = im.crop((left, top, right, bottom))
        im1.save(pngFile)
        png_files[i] = cv2.imread(pngFile)
    im_v = cv2.vconcat(png_files)
    cv2.imwrite(image_file_location + 'concat.png', im_v)

    im = Image.open(image_file_location + "concat.png")
    width, height = im.size
    y = 0
    starting_points = []
    while y < height:
        r,g,b = im.getpixel((45,y))
        if r != 255 and g != 255 and b != 255:
            starting_points.append(y)
            y += 40
        else:
            y += 1

    records = []
    
    for i, starting_point in enumerate(starting_points):
        left = 0
        top = starting_point - 5
        right = width
        if i + 1 == len(starting_points):
            bottom = height
        else:
            bottom = starting_points[i + 1] - 5

        im1 = im.crop((left, top, right, bottom))
        im1.save(image_file_location + 'record_' + str(i) + '.png')
        recordFileName = image_file_location + 'record_' + str(i) + '.png'
    
        fields = ['race_age_and_sex', 'location_officer_and_court']

        record = {}
        for field in fields:
            croppedImgPath = imageCrop(recordFileName, field)
            text = readText(croppedImgPath)
            if field == 'race_age_and_sex':
                age, sex, ethnicities = handle_race_age_and_sex(text)
                record["age"] = age
                record["sex"] = sex
                record["ethnicities"] = ethnicities
            elif field == 'location_officer_and_court':
                locations, officers, courts = handle_location_officer_and_court(text)
                record["locations"] = locations
                record["officers"] = officers
                record["courts"] = courts
        imgFileId = str(uuid.uuid4())
        upload_file(recordFileName, imgFileId + '.png')
        record['id'] = str(uuid.uuid4())
        record['imageId'] = imgFileId + '.png'
        print(record)
        add_record(record)

pdf_splitter(sys.argv[1] + '.pdf')
