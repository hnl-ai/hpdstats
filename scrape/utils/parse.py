# -*- coding: utf-8 -*-
"""The parse utility module."""

import re

from .ocr import correct_ethnicities
from .location import geolocate_location

def get_record_categories():
    """Returns a list of supported parseable categories."""
    return ['race_age_and_sex', 'location_officer_and_court']

def get_dimensions_from_category(category, width):
    """Returns (left, right) dimensions of a certain category section of an image."""
    if category == 'race_age_and_sex':
        return 130, width - 1313
    if category == 'location_officer_and_court':
        return 830, width - 320

def handle_race_age_and_sex(text):
    """Parses the Race/Age/Sex category."""
    race_age_and_sex_output = [text.split('\n')]
    for arr in race_age_and_sex_output:
        arr = [re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', x)
               for x in arr]
        arr = [x for x in arr if x]
        for i, item in enumerate(arr):
            if i % 2 == 1:
                if (len(item.split('/'))) == 2:
                    [sex, age] = item.split('/')
                else:
                    sex = item[0]
                    age = item[-3:-1]
                ethnicities = arr[i - 1].split(',')
                ethnicities = correct_ethnicities(ethnicities)

                return age, sex, ethnicities

def handle_location_officer_and_court(text):
    """Parses the Location/Officer/Court category."""
    location_officer_and_court_output = [text.split('\n\n')]
    result = {
        'locations': [],
        'officers': [],
        'courts': []
    }
    for arr in location_officer_and_court_output:
        arr = [re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', x)
               for x in arr]
        for item in arr:
            item = item.split('\n')
            item = [x for x in item if x]
            if len(item) == 1:
                continue
            while len(item) < 3:
                item.append('')
            [location, officer, court] = item
            location = geolocate_location(location)
            result['locations'].append(location)
            result['officers'].append(officer)
            result['courts'].append(court)
    return (
        result['locations'],
        result['officers'],
        result['courts']
    )

def handle_text_assignment(category, text, record):
    """Wrapper to handle assigning values to categories."""
    if category == 'race_age_and_sex':
        age, sex, ethnicities = handle_race_age_and_sex(text)
        record["age"] = age
        record["sex"] = sex
        record["ethnicities"] = ethnicities
    elif category == 'location_officer_and_court':
        locations, officers, courts = handle_location_officer_and_court(text)
        record["locations"] = locations
        record["officers"] = officers
        record["courts"] = courts
    return record
