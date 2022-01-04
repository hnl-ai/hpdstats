# -*- coding: utf-8 -*-
"""The parse utility module."""

RECORD_WIDTH = 1584  # Width of a record image

# (top, bottom, left, right)
static_category_registry = {
    'date': (0, 25, 40, RECORD_WIDTH - 1450),
    'time': (25, 50, 40, RECORD_WIDTH - 1450),
    'ethnicities': (0, 25, 145, RECORD_WIDTH - 1313),
    'sex': (25, 50, 145, RECORD_WIDTH - 1419),
    'age': (25, 50, 177, RECORD_WIDTH - 1380),
    'name': (0, 25, 270, RECORD_WIDTH - 850)
}


def get_static_record_categories():
    """Returns a list of static positioned supported parseable categories."""
    return static_category_registry.keys()


def get_dimensions_from_static_category(category):
    """Returns (top, bottom, left, right) dimensions of a certain
        static category section of an image."""
    return static_category_registry[category]


# (top, bottom, left, right)
dynamic_category_registry = {
    'report-offense_number': (0, 25, 450, RECORD_WIDTH - 1000),
    'offense_name': (0, 25, 584, RECORD_WIDTH - 770),
    'offense_statute': (25, 50, 584, RECORD_WIDTH - 770),
    'location_of_arrest': (0, 25, 825, RECORD_WIDTH - 315),
    'arrest_officer': (25, 50, 825, RECORD_WIDTH - 315),
    'court_information': (50, 75, 825, RECORD_WIDTH - 315)
}


def get_dynamic_record_categories():
    """Returns a list of dynamically positioned supported parseable categories."""
    return dynamic_category_registry.keys()


def get_dimensions_from_dynamic_category(category):
    """Returns (left, right) dimensions of a certain dynamic category section of an image."""
    return dynamic_category_registry[category]
