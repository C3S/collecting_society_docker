#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the party and company of the collecting society
"""

from proteus import config, Model, Wizard

DEPENDS = [
    'upgrade'
]


def generate():
    # get country
    Country = Model.get('country.country')
    germany, = Country.find([('code', '=', 'DE')])

    # get currency
    Currency = Model.get('currency.currency')
    euro, = Currency.find([('code', '=', 'EUR')])

    # create party
    Party = Model.get('party.party')
    party = Party(name='C3S SCE')
    _ = party.addresses.pop()
    party.addresses.new(
        street='Rochusstraße 44',
        zip='40479',
        city='Düsseldorf',
        country=germany)
    party.save()

    # create company
    Company = Model.get('company.company')
    company_config = Wizard('company.company.config')
    company_config.execute('company')
    company = company_config.form
    company.party = party
    company.currency = euro
    company_config.execute('add')
    company, = Company.find()

    # update context
    User = Model.get('res.user')
    cfg = config.get_config()
    context = User.get_preferences(True, cfg.context)
    context['company'] = 1
    cfg._context = context
