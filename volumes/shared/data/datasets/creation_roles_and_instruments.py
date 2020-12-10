#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the creation roles and instruments
"""

from proteus import  Model

import random
import csv

DEPENDS = [
    'master'
]


def generate(reclimit):
    test_creation_roles = '/shared/data/csv/creation_roles.csv'
    delimiter = ','
    quotechar = '"'
    Artist = Model.get('artist')

    # get Creation Roles
    CreationRole = Model.get('creation.role')
    with open(test_creation_roles, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for role in reader:
            if reclimit and i > reclimit:
                break
            i += 1
            artists = Artist.find([
                ('claim_state', '!=', 'unclaimed'),
                ('group', '!=', True)])
            CreationRole(
                entity_creator=random.choice(artists).party,
                name=role['name'],
                description=role['description']
            ).save()

    # get Instruments
    Instrument = Model.get('instrument')
    with open(test_creation_roles, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for role in reader:
            if reclimit and i > reclimit:
                break
            i += 1
            Instrument(
                name=role['name'],
                description=role['description']
            ).save()