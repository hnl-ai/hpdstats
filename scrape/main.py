# -*- coding: utf-8 -*-
"""The scrape module, containing the HPD arrest log scraper/parser."""

import uuid
import cv2

from .utils.ddb import insert_item
from .utils.imgs import (
    concat_images,
    crop_image,
    convert_pdf_to_png,
    retrieve_image_dimensions,
    retrieve_record_starting_points
)
from .utils.ocr import read_text
from .utils.pdfs import split_into_pages
from .utils.parse import (
    get_record_categories,
    get_dimensions_from_category,
    handle_text_assignment
)
from .utils.s3 import upload_file
from .utils.scrape import check_for_update

IMAGE_DIRECTORY = 'imgs'
RECORDS_BUCKET_NAME = 'honolulupd-records'
RECORDS_TABLE_NAME = 'honolulupd.org-records'

def main(pdf_files):
    """The entry-point main function."""
    for pdf_file in pdf_files:
        pdf_file_pages = split_into_pages(pdf_file)
        img_files = []
        for page in pdf_file_pages:
            img_files.append(convert_pdf_to_png(page))

        for i, img_file in enumerate(img_files):
            width, height = retrieve_image_dimensions(img_file)
            if i == 0:
                left, top, right, bottom = 0, 270, width, height - 100
            else:
                left, top, right, bottom = 0, 160, width, height - 90
            crop_image(img_file, img_file, (left, top, right, bottom))
            img_files[i] = cv2.imread(img_file)
        concat_image = concat_images(img_files)

        record_starting_points = retrieve_record_starting_points(concat_image)
        width, height = retrieve_image_dimensions(concat_image)
        for i, starting_point in enumerate(record_starting_points):
            left, top, right, bottom = 0, starting_point - 5, width, height
            if i + 1 != len(record_starting_points):
                bottom = record_starting_points[i + 1] - 5
            cropped_record_filename = f'{IMAGE_DIRECTORY}/record_{str(i)}.png'
            crop_image(concat_image, cropped_record_filename,
                       (left, top, right, bottom))

            categories = get_record_categories()
            record = {}

            width, height = retrieve_image_dimensions(cropped_record_filename)
            for category in categories:
                top, bottom = 0, height
                left, right = get_dimensions_from_category(category, width)
                cropped_category_filename = f'{IMAGE_DIRECTORY}/record_{str(i)}_{category}.png'
                crop_image(
                    cropped_record_filename,
                    cropped_category_filename,
                    (left,
                     top,
                     right,
                     bottom))
                category_text = read_text(cropped_category_filename)
                record = handle_text_assignment(
                    category, category_text, record)

            img_file_id = str(uuid.uuid4())
            img_filename = f'{img_file_id}.png'
            with open(cropped_record_filename, 'rb') as file:
                upload_file(RECORDS_BUCKET_NAME, img_filename, file, 'image/png')
            record['id'] = str(uuid.uuid4())
            record['imageId'] = img_filename
            print(record)
            insert_item(RECORDS_TABLE_NAME, {
                'date': pdf_file.split('/')[1][0:-4],
                **record
            })

def retrieve_files():
    """Wrapper around the check for new PDF files."""
    pdf_files = check_for_update()
    if len(pdf_files) == 0:
        print('No new PDF files to parse')
        return []
    return pdf_files

if __name__ == "__main__":
    main(retrieve_files())
