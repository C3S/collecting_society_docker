#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the artist playlists
"""

from proteus import Model

DEPENDS = [
    'artist',
]


def generate(reclimit=0):

    # constants
    playlists_per_artist = reclimit or 3

    # models
    Artist = Model.get('artist')
    ArtistPlaylist = Model.get('artist.playlist')

    # entries
    artists = Artist.find([('entity_origin', '=', 'direct')])

    # create artist playlists
    for artist in artists:
        creator = artist.party
        if artist.group:
            creator = artist.solo_artists[0].party
        if not creator:
            continue
        for i in range(playlists_per_artist):
            playlist = ArtistPlaylist(
                artist=artist,
                public=True,
                template=True,
                entity_origin='direct',
                entity_creator=creator
            )
            playlist.save()
