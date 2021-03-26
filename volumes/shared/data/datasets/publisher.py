#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the publishers and publisher parties
"""

from proteus import Model

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # constants
    publisher = reclimit or 10

    # models
    Publisher = Model.get('publisher')
    Party = Model.get('party.party')
    Company = Model.get('company.company')

    # entries
    company, = Company.find([(
        'party.name', '=',
        'C3S SCE'
    )])

    # create publishers
    for i in range(1, publisher + 1):
        if reclimit and i > reclimit:
            break
        number = i
        name = "Publisher %s" % str(number).zfill(3)
        party = Party(name=name)
        party.save()
        Publisher(
            entity_creator=company.party,
            party=party,
            name=name,
        ).save()
