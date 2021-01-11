#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the party and company of the collecting society
"""

import os
import csv

from proteus import config, Model, Wizard

from . import csv_delimiter, csv_quotechar

DEPENDS = [
    'upgrade',
]


def generate(reclimit=0):

    # models
    Country = Model.get('country.country')
    Currency = Model.get('currency.currency')
    Company = Model.get('company.company')
    Party = Model.get('party.party')
    User = Model.get('res.user')

    # wizards
    company_config = Wizard('company.company.config')

    # entries
    euro, = Currency.find([('code', '=', 'EUR')])

    # create party (first row of collecting_socity.csv)
    path = os.path.join('data', 'csv', 'collecting_society.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        row = reader.next()
        country, = Country.find([('code', '=', row['country'])])
        party = Party(name=row['name'])
        _ = party.addresses.pop()
        party.addresses.new(
            street=row['street'],
            zip=row['zip'],
            city=row['city'],
            country=country
        )
        party.save()

    # create company
    company_config.execute('company')
    company = company_config.form
    company.party = party
    company.currency = euro
    company_config.execute('add')
    company, = Company.find()

    # update context
    cfg = config.get_config()
    context = User.get_preferences(True, cfg.context)
    context['company'] = 1
    cfg._context = context
