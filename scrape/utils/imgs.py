# -*- coding: utf-8 -*-
"""The image utility module."""

import os

import cv2
import fitz
from PIL import Image

IMAGE_DIRECTORY = 'imgs'

def concat_images(images):
    """Vertically concatenates all the records into one long vertical record: concat.png"""
    vertical_images = cv2.vconcat(images)
    output_filename = f'{IMAGE_DIRECTORY}/concat.png'
    cv2.imwrite(output_filename, vertical_images)
    return output_filename

def convert_pdf_to_png(pdf_file_path):
    """Converts the given PDF file to a PNG file."""
    doc = fitz.open(pdf_file_path)
    mat = fitz.Matrix(2, 2)
    page = doc.loadPage(0)
    pix = page.getPixmap(matrix=mat)

    output_filename = f'{IMAGE_DIRECTORY}/{os.path.basename(pdf_file_path)}.png'
    pix.writePNG(output_filename)
    return output_filename

def crop_image(img, cropped_img, dimensions):
    """Crops the given image to the provided dimensions."""
    image = Image.open(img)
    cropped_image = image.crop(dimensions)
    cropped_image.save(cropped_img)
    return cropped_image

def retrieve_image_dimensions(img):
    """Retrieves the dimensions of the given image (width/height)."""
    image = Image.open(img)
    width, height = image.size
    return width, height

def retrieve_record_starting_points(img):
    """Finds all the records starting points by looking for pixels on each line."""
    image = Image.open(img)
    _, height = image.size

    current_y = 0
    starting_points = []

    while current_y < height:
        red, green, blue = image.getpixel((45, current_y))
        if red != 255 and green != 255 and blue != 255: # Starting line of a record has been found
            starting_points.append(current_y)
            current_y += 40 # Move forward to the next area of records
        else:
            current_y += 1

    return starting_points
