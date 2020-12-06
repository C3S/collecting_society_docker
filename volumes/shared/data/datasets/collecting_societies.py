#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the collecting societies
"""

from proteus import  Model

DEPENDS = [
    'master'
]


def generate():
    # get company and collecting society
    CollectingSociety = Model.get('collecting_society')
    Company = Model.get('company.company')
    company = Company(1)

    # get country
    Country = Model.get('country.country')
    germany, = Country.find([('code', '=', 'DE')])

    # get party
    Party = Model.get('party.party')

    # C3S
    CollectingSociety(
        name=company.party.name,
        party=company.party,
        represents_copyright=True,
        represents_ancillary_copyright=True
    ).save()

    # GEMA

    party = Party(name='GEMA')
    _ = party.addresses.pop()
    party_address = party.addresses.new(
        street='Bayreuther Straße 37',
        zip='10787',
        city='Berlin',
        country=germany
    )
    party.save()
    CollectingSociety(
        name=party.name,
        party=party,
        represents_copyright=True,
        represents_ancillary_copyright=False
    ).save()

    # GVL

    party = Party(name='GVL')
    _ = party.addresses.pop()
    party.addresses.new(
        street='Podbielskiallee 64',
        zip='14195',
        city='Berlin',
        country=germany
    )
    party.save()
    CollectingSociety(
        name=party.name,
        party=party,
        represents_copyright=False,
        represents_ancillary_copyright=True
    ).save()
