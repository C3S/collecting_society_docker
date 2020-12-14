#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create identifier
"""

from proteus import Model

import csv

DEPENDS = [
    'master'
]


def generate(reclimit):

    # models
    Artist = Model.get('artist')
    ArtistIdentifier = Model.get('artist.identifier')
    ArtistIdentifierSpace = Model.get('artist.identifier.space')
    Creation = Model.get('creation')
    CreationIdentifier = Model.get('creation.identifier')
    CreationIdentifierSpace = Model.get('creation.identifier.space')
    Release = Model.get('release')
    ReleaseIdentifier = Model.get('release.identifier')
    ReleaseIdentifierSpace = Model.get('release.identifier.space')
    Party = Model.get('party.party')
    PartyIdentifier = Model.get('party.identifier')
    PartyIdentifierSpace = Model.get('party.identifier.space')

    # party identifiers
    parties = Party.find([])
    space_ipi, = PartyIdentifierSpace.find(
        [('name', '=', 'IPI')])
    space_isni, = PartyIdentifierSpace.find(
        [('name', '=', 'ISNI')])
    space_ddexpi, = PartyIdentifierSpace.find(
        [('name', '=', 'DDEX Party Identifier')])
    # TODO: PartyIdentifierSpace is empty by now, find should return []

    for i in range(1, len(parties) + 1):
        number = i
        party = parties[i - 1]
        # ipi
        identifier = PartyIdentifier(
            party = party,
            space = space_ipi,
            id_code = "%s" % str(number).zfill(11)
        ).save()
        # isni
        identifier = PartyIdentifier(
            party = party,
            space = space_isni,
            id_code = "%s" % str(number).zfill(16)
        ).save()
        # ddexpi
        identifier = PartyIdentifier(
            party = party,
            space = space_ddexpi,
            id_code = "%s-%s-%s-%s" % (
                'PA', 'DPIDA', str(number).zfill(10), 'G'
            )
        ).save()

    # artist identifiers
    artists = Artist.find([])
    space_ipn, = ArtistIdentifierSpace.find(
        [('name', '=', 'IPN')])

    for i in range(1, len(artists) + 1):
        number = i
        artist = artists[i - 1]
        # ipn
        identifier = ArtistIdentifier(
            artist = artist,
            space = space_ipn,
            id_code = "%s" % str(number).zfill(11)
        ).save()

    # release identifiers
    releases = Release.find([])
    space_grid, = ReleaseIdentifierSpace.find(
        [('name', '=', 'GRid')])
    space_eanupc, = ReleaseIdentifierSpace.find(
        [('name', '=', 'EAN/UPC')])

    for i in range(1, len(releases) + 1):
        number = i
        release = releases[i - 1]
        # grid
        identifier = ReleaseIdentifier(
            release = release,
            space = space_grid,
            id_code = "%s-%s-%s-%s" % (
                'A1', 'ABCDE', str(number).zfill(10), 'M'
            )
        ).save()
        # eanupc
        identifier = ReleaseIdentifier(
            release = release,
            space = space_eanupc,
            id_code = "%s" % str(number).zfill(13)
        ).save()

    # creation identifiers
    creations = Creation.find([])
    space_hfa, = CreationIdentifierSpace.find(
        [('name', '=', 'HFA Song Code')])
    space_isrc, = CreationIdentifierSpace.find(
        [('name', '=', 'ISRC')])
    space_iswc, = CreationIdentifierSpace.find(
        [('name', '=', 'ISWC')])
    space_cwr, = CreationIdentifierSpace.find(
        [('name', '=', 'CWR')])

    for i in range(1, len(creations) + 1):
        number = i
        creation = creations[i - 1]
        # hfa
        identifier = CreationIdentifier(
            creation = creation,
            space = space_hfa,
            id_code = "%s" % str(number).zfill(6)
        ).save()
        # isrc
        identifier = CreationIdentifier(
            creation = creation,
            space = space_isrc,
            id_code = "%s-%s-%s-%s" % (
                'DE', 'A00', '20', str(number).zfill(5)
            )
        ).save()
        # iswc
        identifier = CreationIdentifier(
            creation = creation,
            space = space_iswc,
            id_code = "%s-%s.%s.%s-%s" % (
                'T',
                str(number / 1000000).zfill(3),
                str(number / 1000).zfill(3),
                str(number % 1000).zfill(3),
                'C'
            )
        ).save()
        # cwr
        identifier = CreationIdentifier(
            creation = creation,
            space = space_cwr,
            id_code = "%s%s%s%s_%s.V%s" % (
                'CW', 20, str(number).zfill(4), 'SSS', 'RRR', 21
            )
        ).save()
