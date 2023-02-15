#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the licenses
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar, csv_devlimit

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # constants
    environment = os.environ.get('ENVIRONMENT')
    if environment == "development":
        reclimit = reclimit and min(reclimit, csv_devlimit) or csv_devlimit

    # models
    License = Model.get('license')

    # create licenses
    path = os.path.join('data', 'csv', 'license.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for i, row in enumerate(reader):
            if reclimit and i == reclimit:
                break
            License(
                code=row['code'],
                version=row['version'],
                country=row['country'],
                freedom_rank=int(row['freedom_rank']),
                link=row['link'],
                name=row['name']
            ).save()
