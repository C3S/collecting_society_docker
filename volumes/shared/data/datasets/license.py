#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create licenses
"""

from proteus import  Model

import csv

DEPENDS = [
    'master'
]


def generate(reclimit):
    test_licenses = '/shared/data/csv/licenses.csv'
    delimiter = ','
    quotechar = '"'

    # get licenses
    License = Model.get('license')
    with open(test_licenses, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for license in reader:
            if reclimit and i > reclimit:
                break
            i += 1
            License(
                code=license['code'],
                version=license['version'],
                country=license['country'],
                freedom_rank=int(license['freedom_rank']),
                link=license['link'],
                name=license['name']
            ).save()
