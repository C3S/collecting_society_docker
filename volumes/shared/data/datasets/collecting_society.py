#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the collecting societies
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
    Country = Model.get('country.country')
    Party = Model.get('party.party')
    CollectingSociety = Model.get('collecting_society')

    # create collecting societies
    path = os.path.join('data', 'csv', 'collecting_society.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for i, row in enumerate(reader):
            if reclimit and i == reclimit:
                break
            party = Party.find(['name', '=', row['name']])
            if party:
                party = party[0]
            else:
                country, = Country.find([('code', '=', row['country'])])
                party = Party(name=row['name'])
                _ = party.addresses.pop()
                party.addresses.new(
                    street=row['street'],
                    postal_code=row['postal_code'],
                    city=row['city'],
                    country=country
                )
                party.save()
            CollectingSociety(
                name=party.name,
                party=party,
                represents_copyright=bool(
                    int(row['copyright'])),
                represents_ancillary_copyright=bool(
                    int(row['ancillary_copyright']))
            ).save()
