#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the artist playlist items
"""

import random

from proteus import Model

DEPENDS = [
    'creation',
    'artist_playlist',
]


def generate(reclimit=0):

    # constants
    artist_creations_per_playlist = reclimit or 8
    foreign_creations_per_playlist = reclimit or 2

    # models
    ArtistPlaylist = Model.get('artist.playlist')
    ArtistPlaylistItem = Model.get('artist.playlist.item')
    Creation = Model.get('creation')

    # entries
    playlists = ArtistPlaylist.find([])

    # create artist playlist items
    for playlist in playlists:
        creations = Creation.find([('artist.id', '=', playlist.artist.id)])
        artist_items = random.sample(
            creations, min(artist_creations_per_playlist, len(creations))
        )
        creations = Creation.find([('artist.id', '!=', playlist.artist.id)])
        foreign_items = random.sample(
            creations, min(foreign_creations_per_playlist, len(creations))
        )
        for i, item in enumerate(artist_items + foreign_items, start=1):
            ArtistPlaylistItem(
                playlist=playlist,
                creation=item,
                position=i,
                entity_origin='direct',
                entity_creator=playlist.entity_creator
            ).save()
