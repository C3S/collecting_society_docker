#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the party identifiers
"""

from proteus import Model

DEPENDS = [
    'artist',
    'collecting_society',
    'publisher',
    'label',
]


def generate(reclimit=0):

    # models
    Party = Model.get('party.party')
    PartyIdentifierSpace = Model.get('party.identifier.space')

    # entries
    parties = Party.find([])
    space_ipi, = PartyIdentifierSpace.find(
        [('name', '=', 'IPI')])
    space_isni, = PartyIdentifierSpace.find(
        [('name', '=', 'ISNI')])
    space_ddexpi, = PartyIdentifierSpace.find(
        [('name', '=', 'DDEX Party Identifier')])

    # create party identifiers
    for i, party in enumerate(parties, start=1):

        # ipi
        ipi = party.identifiers.new()
        ipi.space = space_ipi
        ipi.id_code = "%s" % str(i).zfill(11)

        # isni
        isni = party.identifiers.new()
        isni.space = space_isni
        isni.id_code = "%s" % str(i).zfill(16)

        # ddexpi
        ddexpi = party.identifiers.new()
        ddexpi.space = space_ddexpi
        ddexpi.id_code = "%s-%s-%s-%s" % (
            'PA', 'DPIDA', str(i).zfill(10), 'G'
        )

        party.save()
