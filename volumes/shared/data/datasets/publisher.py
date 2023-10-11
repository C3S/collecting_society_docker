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
    Account = Model.get('account.account')

    # entries
    company, = Company.find([(
        'party.name', '=',
        'C3S SCE'
    )])
    receivable, = Account.find([
            ('type.receivable', '=', True),
            ('party_required', '=', True),
            ('company', '=', company.id),
            ], limit=1)
    payable, = Account.find([
            ('type.payable', '=', True),
            ('party_required', '=', True),
            ('company', '=', company.id),
            ], limit=1)

    # create publishers
    for i in range(1, publisher + 1):
        if reclimit and i > reclimit:
            break
        number = i
        name = "Publisher %s" % str(number).zfill(3)
        party = Party(name=name)
        party.account_receivable = receivable
        party.account_payable = payable
        party.save()
        Publisher(
            entity_creator=company.party,
            party=party,
            name=name,
        ).save()
