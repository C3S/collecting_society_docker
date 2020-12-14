#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create label
"""

from proteus import  Model

import csv

DEPENDS = [
    'collecting_societies'  # misuses C3S for party, TODO: real label parties
]


def generate(reclimit):
    test_labels = '/shared/data/csv/labels.csv'
    delimiter = ','
    quotechar = '"'

    # get labels
    Label = Model.get('label')
    Company = Model.get('company.company')
    company, = Company.find([(
        'party.name', '=',
        'C3S SCE'
    )])
    with open(test_labels, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for label in reader:
            if reclimit and i > reclimit:
                break
            i += 1
            Label(
                entity_creator=company.party,
                name=label['name'],
                gvl_code=label['gvl_code']
            ).save()