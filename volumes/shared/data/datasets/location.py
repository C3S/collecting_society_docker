#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create location
"""

from proteus import Model

import csv

DEPENDS = [
    'master'
]


def generate(reclimit):

    # constants
    test_location_categories = '/shared/data/csv/location_categories.csv'
    test_location_space_categories = '/shared/data/csv/location_space_categories.csv'
    delimiter = ','
    quotechar = '"'

    # models
    LocationCategory = Model.get('location.category')
    LocationSpaceCategory = Model.get('location.space.category')

    # location categories
    with open(test_location_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            LocationCategory(
                name=category['name'],
                code=category['code'],
                description=category['description']
            ).save()

    # location space categories
    with open(test_location_space_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            LocationSpaceCategory(
                name=category['name'],
                code=category['code'],
                description=category['description']
            ).save()
