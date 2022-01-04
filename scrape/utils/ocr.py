# -*- coding: utf-8 -*-
"""The optical character recognition utility module."""

import re

import pytesseract
from PIL import Image


def correct_ethnicities(ethnicities):
    """Corrects a list of OCR misread ethnicities into their proper category."""
    ethnicities = list(filter(None, ethnicities))
    ethnicities = [x.strip() for x in ethnicities]
    corrections = {
        "Filipino": ["Filipi", "Filipir", "Filig", "Filip", "Filipit"],
        "Hawaiian": ["Hawe", "Haw:", "Hawai", "Hawaiia", "Hawaiie", "Hav"],
        "Samoan": ["Sam", "Samc", "Samo:", "San", "Sarn",
            "Sar", "Samoar", "Samoi", "Sarr"],
        "Hispanic": ["Hispani", "Hispani:", "Hispanir", "Hispaniv"],
        "Other": ["Othe", "Othe:", "Other Pac. Isl", "Othe!",
            "Other Pac. Isl:", "Other P", "Other A", "Other Asian"],
        "Unknown": ["H", "C", "Unkr"],
        "Indian": ["India", "Indiai"],
        "Japanese": ["Jap", "Jap:", "Jap<", "Japa", "Japane:", "Japan", "Japai", "Japanes"],
        "Native American": ["Native Americ", "Native", "Nativ", "Native /"],
        "Chinese": ["Chin"],
        "Tongan": ["Ton:", "Ton", "Tong"],
        "Micronesian": ["Mic", "Micr", "Micrc", "Microne", "Micror"],
        "Laotian": ["Laotia"],
        "Middle Eastern": ["Middle Easter", "Middle Easter:"],
        "Black": ["Blac"],
        "Korean": ["Kor", "Kore", "Kore:"],
        "White": ["Whi", "Whi!", "Whit", "Whit:"]
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
    return pytesseract.image_to_string(Image.open(path), config='--psm 10')


def clean_text(text):
    """Cleans the OCR read text."""
    # 1. Remove trailing hex characters ex: "\x07"
    cleaned_text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', text)
    # 2. Strip newline characters ex: "\n"
    cleaned_text = cleaned_text.strip()
    return cleaned_text
