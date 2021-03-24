#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the artist identifiers
"""

from proteus import Model

DEPENDS = [
    'artist',
]


def generate(reclimit=0):

    # models
    Artist = Model.get('artist')
    ArtistIdentifierSpace = Model.get('artist.identifier.space')

    # entries
    artists = Artist.find([])
    space_ipn, = ArtistIdentifierSpace.find([('name', '=', 'IPN')])

    # create artist identifiers
    for i, artist in enumerate(artists, start=1):

        # ipn
        ipn = artist.identifiers.new()
        ipn.space = space_ipn
        ipn.id_code = "%s" % str(i).zfill(11)

        artist.save()
