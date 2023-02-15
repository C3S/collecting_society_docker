#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the creation identifiers
"""

from proteus import Model

DEPENDS = [
    'creation',
]


def generate(reclimit=0):

    # models
    Creation = Model.get('creation')
    CreationIdentifierSpace = Model.get('creation.cs_identifier.space')

    # entries
    creations = Creation.find([])
    space_hfa, = CreationIdentifierSpace.find([('name', '=', 'HFA Song Code')])
    space_isrc, = CreationIdentifierSpace.find([('name', '=', 'ISRC')])
    space_iswc, = CreationIdentifierSpace.find([('name', '=', 'ISWC')])
    space_cwr, = CreationIdentifierSpace.find([('name', '=', 'CWR')])

    # create creation identifiers
    for i, creation in enumerate(creations, start=1):

        # hfa
        hfa = creation.cs_identifiers.new()
        hfa.space = space_hfa
        hfa.id_code = "%s" % str(i).zfill(6)

        # isrc
        isrc = creation.cs_identifiers.new()
        isrc.space = space_isrc
        isrc.id_code = "%s-%s-%s-%s" % (
            'DE', 'A00', '20', str(i).zfill(5)
        )

        # iswc
        iswc = creation.cs_identifiers.new()
        iswc.space = space_iswc
        iswc.id_code = "%s-%s.%s.%s-%s" % (
            'T',
            str(i / 1000000).zfill(3),
            str(i / 1000).zfill(3),
            str(i % 1000).zfill(3),
            'C'
        )

        # cwr
        cwr = creation.cs_identifiers.new()
        cwr.space = space_hfa
        cwr.id_code = "%s%s%s%s_%s.V%s" % (
            'CW', 20, str(i).zfill(4), 'SSS', 'RRR', 21
        )

        creation.save()
