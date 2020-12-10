#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create publisher
"""

from proteus import  Model

DEPENDS = [
    'master'
]


def generate(reclimit):
    publisher = reclimit or 10
    Publisher = Model.get('publisher')
    Party = Model.get('party.party')
    Company = Model.get('company.company')
    company, = Company.find([(
        'party.name', '=',
        'C3S SCE'
    )])
    for i in range(1, publisher + 1):
        number = i
        name = "Publisher %s" % str(number).zfill(3)
        party = Party(name=name)
        party.save()
        Publisher(
            entity_creator=company.party,
            party=party,
            name=name,
        ).save()