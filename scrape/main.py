# -*- coding: utf-8 -*-
"""The scrape module, containing the HPD arrest log scraper/parser."""

import os
import uuid

import cv2

import constants

from utils.ddb import insert_item
from utils.imgs import (
    concat_images,
    crop_image,
    convert_pdf_to_png,
    retrieve_image_dimensions,
    retrieve_record_starting_points,
    retrieve_offense_starting_points
)
from utils.ocr import clean_text, read_text, correct_ethnicities
from utils.pdfs import split_into_pages, initialize_pdf_directory
from utils.parse import (
    get_static_record_categories,
    get_dynamic_record_categories,
    get_dimensions_from_static_category,
    get_dimensions_from_dynamic_category
)
from utils.s3 import upload_file
from utils.scrape import check_for_update
from utils.location import geolocate_location
from utils.files import copy_file, zip_directory


def main(pdf_files):
    """The entry-point main function."""
    for pdf_file in pdf_files:
        pdf_directory_registry = initialize_pdf_directory(
            os.path.splitext(pdf_file[5:])[0])
        copy_file_path = f"{pdf_directory_registry['root']}/index.pdf"
        copy_file(pdf_file, copy_file_path)
        manifest_file_path = f"{pdf_directory_registry['root']}/manifest.txt"
        with open(manifest_file_path, 'w', encoding='utf-8') as manifest_file:
            manifest_file.write('ARREST LOG MANIFEST\n')

        pdf_file_pages = split_into_pages(
            pdf_directory_registry['pages'], pdf_file)

        image_files = []
        for page in pdf_file_pages:
            image_files.append(
                convert_pdf_to_png(
                    pdf_directory_registry['images'],
                    page
                )
            )

        for i, img_file in enumerate(image_files):
            # Crop the headers and footers out of each page
            width, height = retrieve_image_dimensions(img_file)
            if i == 0:
                left, top, right, bottom = 0, 270, width, height - 100
            else:
                left, top, right, bottom = 0, 160, width, height - 90
            crop_image(img_file, img_file, (left, top, right, bottom))
            image_files[i] = cv2.imread(img_file)
        concat_image = concat_images(
            pdf_directory_registry['images'],
            image_files
        )
        record_starting_points = retrieve_record_starting_points(concat_image)

        print(f'# of records detected: {len(record_starting_points)}')
        with open(manifest_file_path, 'a', encoding='utf-8') as manifest_file:
            manifest_file.write(f'# of records: {len(record_starting_points)}\n')

        width, height = retrieve_image_dimensions(concat_image)
        records = []
        for i, starting_point in enumerate(record_starting_points):
            left, top, right, bottom = 0, starting_point - 5, width, height
            if i + 1 != len(record_starting_points):
                bottom = record_starting_points[i + 1] - 5
            records_subdir = pdf_directory_registry['records']
            cropped_record_filename = f'{records_subdir}/{str(i + 1)}.png'
            records.append(crop_image(
                concat_image,
                cropped_record_filename,
                (left, top, right, bottom)
            ))

        total_offenses_count = 0
        for i, record_image_path in enumerate(records):
            print(record_image_path)
            record_data = {}

            # START - ITERATE OVER STATIC CATEGORIES - START
            static_categories = get_static_record_categories()

            for category in static_categories:
                top, bottom, left, right = get_dimensions_from_static_category(
                    category)
                cropped_category_filename = \
                    f'{constants.PDF_TMP_DIRECTORY}/record_{str(i + 1)}_{category}.png'
                crop_image(
                    record_image_path,
                    cropped_category_filename,
                    (left,
                     top,
                     right,
                     bottom))
                category_text = read_text(cropped_category_filename)
                record_data[category] = clean_text(category_text)

            # END - ITERATE OVER STATIC CATEGORIES - END

            # START - ITERATE OVER DYNAMIC CATEGORIES - START

            offenses_starting_points = retrieve_offense_starting_points(
                record_image_path)
            total_offenses_count += len(offenses_starting_points)
            print(f'# of offenses detected: {len(offenses_starting_points)}')

            offenses = []
            for j, offense_starting_point in enumerate(
                    offenses_starting_points):
                left, top, right, bottom = 0, offense_starting_point - 5, width, height
                if j + 1 != len(offenses_starting_points):
                    bottom = offenses_starting_points[j + 1] - 5
                cropped_offense_filename = \
                    f'{constants.PDF_TMP_DIRECTORY}/record_{str(i + 1)}_offense_{str(j + 1)}.png'
                offenses.append(crop_image(
                    record_image_path,
                    cropped_offense_filename,
                    (left, top, right, bottom)
                ))

            dynamic_categories = get_dynamic_record_categories()
            for category in dynamic_categories:
                record_data[category] = []

            for offense_file_path in offenses:
                for category in dynamic_categories:
                    top, bottom, left, right = get_dimensions_from_dynamic_category(
                        category)
                    cropped_category_filename = \
                        f'{constants.PDF_TMP_DIRECTORY}/record_{str(i + 1)}_{category}.png'
                    crop_image(
                        offense_file_path,
                        cropped_category_filename,
                        (left,
                         top,
                         right,
                         bottom))
                    category_text = read_text(cropped_category_filename)
                    record_data[category].append(clean_text(category_text))

            # END - ITERATE OVER DYNAMIC CATEGORIES - END

            # Convert "ethnicities" string to an array of strings
            # "White, Tongan" -> ["White", "Tongan"]
            record_data['ethnicities'] = record_data['ethnicities'].split(',')
            record_data['ethnicities'] = correct_ethnicities(
                record_data['ethnicities'])

            # Geolocate the locations
            locations = []
            for location in record_data['location_of_arrest']:
                locations.append(geolocate_location(location))
            record_data['locations'] = locations

            img_file_id = str(uuid.uuid4())
            img_filename = f'{img_file_id}.png'
            with open(record_image_path, 'rb') as file:
                upload_file(
                    constants.RECORDS_BUCKET_NAME,
                    img_filename,
                    file,
                    'image/png')
            record_data['id'] = str(uuid.uuid4())
            record_data['imageId'] = img_filename
            print(record_data)
            insert_item(constants.RECORDS_TABLE_NAME, {
                'date': pdf_file.split('/')[1][0:-4],
                **record_data
            })

        with open(manifest_file_path, 'a', encoding='utf-8') as manifest_file:
            manifest_file.write(f'# of offenses: {total_offenses_count}\n')

        output_zip_file = f"{constants.PDF_TMP_DIRECTORY}/{pdf_file.split('/')[1][0:-4]}"
        zip_directory(output_zip_file, pdf_directory_registry['root'])
        with open(output_zip_file + '.zip', 'rb') as file:
            upload_file(constants.ARTIFACTS_BUCKET_NAME, pdf_file.split(
                '/')[1][0:-4] + '.zip', file, 'application/zip')


def retrieve_files():
    # """Wrapper around the check for new PDF files."""
    # pdf_files = check_for_update()
    # if len(pdf_files) == 0:
    #     print('No new PDF files to parse')
    #     return []
    # return pdf_files
    from os import listdir
    from os.path import isfile, join
    onlyfiles = ['pdfs/' + f for f in listdir('pdfs/') if isfile(join('pdfs/', f)) and f.endswith('pdf')]

    return sorted(onlyfiles)

if __name__ == '__main__':
    main(retrieve_files())
