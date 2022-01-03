# -*- coding: utf-8 -*-
"""The image utility module."""

import os

import cv2
import fitz
from PIL import Image


def concat_images(image_subdir, images):
    """Vertically concatenates all the records into one long vertical record: concat.png"""
    vertical_images = cv2.vconcat(images)
    output_filename = f'{image_subdir}/vconcat.png'
    cv2.imwrite(output_filename, vertical_images)
    return output_filename


def convert_pdf_to_png(image_subdir, pdf_file_path):
    """Converts the given PDF file to a PNG file."""
    doc = fitz.open(pdf_file_path)
    mat = fitz.Matrix(2, 2)
    page = doc.loadPage(0)
    pix = page.getPixmap(matrix=mat)

    image_file_name = os.path.splitext(pdf_file_path)[0]
    output_filename = f'{image_subdir}/{os.path.basename(image_file_name)}.png'
    pix.writePNG(output_filename)
    return output_filename


def crop_image(img, cropped_img_path, dimensions):
    """Crops the given image to the provided dimensions."""
    image = Image.open(img)
    cropped_image = image.crop(dimensions)
    cropped_image.save(cropped_img_path)
    return cropped_img_path


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
        if red != 255 and green != 255 and blue != 255:  # Starting line of a record has been found
            starting_points.append(current_y)
            current_y += 40  # Move forward to the next area of records
        else:
            current_y += 1

    return starting_points


def retrieve_offense_starting_points(img):
    """Finds all the offenses starting points in a record by looking for pixels on each line."""
    image = Image.open(img)
    _, height = image.size

    current_y = 20
    starting_points = []

    while current_y < height:
        red, green, blue = image.getpixel((460, current_y))
        if red != 255 and green != 255 and blue != 255: # Starting line of an offense has been found
            starting_points.append(current_y)
            current_y += 40  # Move forward to the next area of offenses
        else:
            current_y += 1

    return starting_points
