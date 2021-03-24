#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the location categories
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar

DEPENDS = [
    'master',
]


def generate(reclimit=0):

    # models
    LocationCategory = Model.get('location.category')

    # create location categories
    path = os.path.join('data', 'csv', 'location_category.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for i, row in enumerate(reader):
            LocationCategory(
                name=row['name'],
                code=row['code'],
                description=row['description']
            ).save()
