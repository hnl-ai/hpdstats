# -*- coding: utf-8 -*-
"""The optical character recognition utility module."""

import pytesseract
from PIL import Image

def correct_ethnicities(ethnicities):
    """Corrects a list of OCR misread ethnicities into their proper category."""
    ethnicities = list(filter(None, ethnicities))
    ethnicities = [x.strip() for x in ethnicities]
    corrections = {
        "Filipino": ["Filipi", "Filipir"],
        "Hawaiian": ["Hawe", "Haw:", "Hawai", "Hawaiia", "Hawaiie", "Hav"],
        "Samoan": ["Sar", "Samoar", "Samoi", "Sarr"],
        "Hispanic": ["Hispani", "Hispani:", "Hispanir"],
        "Other": ["Othe", "Othe:", "Other Pac. Isl", "Other Pac. Isl:", "Other P", "Other Asian"],
        "Unknown": ["H", "C", "Unkr"],
        "Indian": ["India"],
        "Japanese": ["Japa", "Japane:", "Japan", "Japai", "Japanes"],
        "Native American": ["Native Americ", "Native"],
        "Chinese": ["Chin"],
        "Tongan": ["Ton", "Tong"],
        "Micronesian": ["Micr"],
        "Laotian": ["Laotia"],
        "Middle Eastern": ["Middle Easter", "Middle Easter:"]
    }
    corrected_ethnicities = []

    for ethnicity in ethnicities:
        inserted = False
        for correction, wrongs in corrections.items():
            if ethnicity in wrongs:
                corrected_ethnicities.append(correction)
                inserted = True
        if not inserted:
            corrected_ethnicities.append(ethnicity)

    return corrected_ethnicities

def read_text(path):
    """Reads the text of the given image."""
    return pytesseract.image_to_string(Image.open(path))
