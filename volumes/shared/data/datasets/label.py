#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the labels and label parties
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar, csv_devlimit

DEPENDS = [
    'master',
]


def generate(reclimit=0):

    # constants
    environment = os.environ.get('ENVIRONMENT')
    if environment == "development":
        reclimit = reclimit and min(reclimit, csv_devlimit) or csv_devlimit

    # models
    Party = Model.get('party.party')
    Company = Model.get('company.company')
    Label = Model.get('label')

    # entries
    company = Company(1)

    # create labels
    path = os.path.join('data', 'csv', 'label.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for i, row in enumerate(reader):
            if reclimit and i == reclimit:
                break
            party = Party(name=row['name'])
            party.save()
            Label(
                entity_creator=company.party,
                name=row['name'],
                party=party,
                gvl_code=row['gvl_code']
            ).save()
