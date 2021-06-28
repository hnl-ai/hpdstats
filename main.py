from ddb_utils import insert_item
from img_utils import concat_images, crop_image, convert_pdf_to_png, retrieve_image_dimensions, retrieve_record_starting_points
from ocr_utils import read_text
from pdf_utils import split_into_pages
from record_utils import get_record_categories, get_dimensions_from_category, handle_text_assignment
from s3_utils import upload_file
from scrape_utils import check_for_update

import cv2
import uuid

image_directory_location = 'imgs'
records_bucket_name = 'honolulupd-records'
records_table_name = 'honolulupd.org-records'


def main():
    pdf_files = check_for_update()
    if len(pdf_files) == 0:
        return print('No new PDF files to parse')

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
            cropped_record_filename = '{}/record_{}.png'.format(image_directory_location, str(i))
            crop_image(concat_image, cropped_record_filename, (left, top, right, bottom))

            categories = get_record_categories()
            record = {}

            width, height = retrieve_image_dimensions(cropped_record_filename)
            for category in categories:
                top, bottom = 0, height
                left, right = get_dimensions_from_category(category, width)
                cropped_category_filename = '{}/record_{}_{}.png'.format(image_directory_location, str(i), category)
                crop_image(cropped_record_filename, cropped_category_filename, (left, top, right, bottom))
                category_text = read_text(cropped_category_filename)
                record = handle_text_assignment(category, category_text, record)

            img_file_id = str(uuid.uuid4())
            img_filename = '{}.png'.format(img_file_id)
            with open(cropped_record_filename, 'rb') as f:
                upload_file(records_bucket_name, img_filename, f, 'image/png')
            record['id'] = str(uuid.uuid4())
            record['imageId'] = img_filename
            print(record)
            insert_item(records_table_name, {
                'date': pdf_file.split('/')[1][0:-4],
                **record
            })


if __name__ == "__main__":
    main()
