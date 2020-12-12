#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create artist playlist
"""

from proteus import Model

import random

DEPENDS = [
    'artist'
]


def generate(reclimit):

    # constants
    playlists_per_artist = reclimit or 3
    artist_creations_per_playlist = reclimit or 8
    foreign_creations_per_playlist = reclimit or 2

    # models
    Artist = Model.get('artist')
    ArtistPlaylist = Model.get('artist.playlist')
    ArtistPlaylistItem = Model.get('artist.playlist.item')
    Creation = Model.get('creation')

    artists = Artist.find([('entity_origin', '=', 'direct')])
    for artist in artists:
        party = artist.party
        if artist.group:
            party = artist.solo_artists[0].party
        if not party:
            continue
        for i in range(0, playlists_per_artist):
            # playlist
            playlist = ArtistPlaylist(
                artist=artist,
                public=True,
                template=True,
                entity_origin='direct',
                entity_creator=party
            )
            playlist.save()
            # playlist items
            creations = Creation.find([('artist.id', '=', artist.id)])
            artist_items = random.sample(
                creations,
                min(artist_creations_per_playlist, len(creations))
            )
            creations = Creation.find([('artist.id', '!=', artist.id)])
            foreign_items = random.sample(
                creations,
                min(foreign_creations_per_playlist, len(creations))
            )
            for i, item in enumerate(artist_items + foreign_items):
                ArtistPlaylistItem(
                    playlist=playlist,
                    creation=item,
                    position=i + 1,
                    entity_origin='direct',
                    entity_creator=party
                ).save()