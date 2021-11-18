import os

import cv2
import fitz
from PIL import Image

image_directory_location = 'imgs'


# Vertically concatenates all the records into one long vertical record:
# "concat.png"
def concat_images(images):
    vertical_images = cv2.vconcat(images)
    output_filename = '{}/concat.png'.format(image_directory_location)
    cv2.imwrite(output_filename, vertical_images)
    return output_filename


def convert_pdf_to_png(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    mat = fitz.Matrix(2, 2)
    page = doc.loadPage(0)
    pix = page.getPixmap(matrix=mat)

    output_filename = '{}/{}.png'.format(
        image_directory_location,
        os.path.basename(pdf_file_path))
    pix.writePNG(output_filename)
    return output_filename


def crop_image(img, cropped_img, dimensions):
    image = Image.open(img)
    cropped_image = image.crop(dimensions)
    cropped_image.save(cropped_img)
    return cropped_image


def retrieve_image_dimensions(img):
    image = Image.open(img)
    width, height = image.size
    return width, height


# Finds all the records' starting points by looking for pixels on each line
def retrieve_record_starting_points(img):
    image = Image.open(img)
    width, height = image.size

    y = 0
    starting_points = []

    while y < height:
        r, g, b = image.getpixel((45, y))
        if r != 255 and g != 255 and b != 255:
            starting_points.append(y)
            y += 40
        else:
            y += 1

    return starting_points
