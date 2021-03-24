#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the artist public/performance playlists
"""

from proteus import Model

DEPENDS = [
    'event_performance',
]


def generate(reclimit=0):

    # constants
    playlists_per_artist = reclimit or 3

    # models
    Artist = Model.get('artist')
    ArtistPlaylist = Model.get('artist.playlist')
    EventPerformance = Model.get('event.performance')

    # entries
    artists = Artist.find([('entity_origin', '=', 'direct')])
    performances = EventPerformance.find([])

    # create public playlists
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

    # create performance playlists
    for performance in performances:
        playlist = ArtistPlaylist(
            artist=performance.artist,
            public=False,
            template=False,
            performance=[performance],
            entity_origin='indirect',
            entity_creator=performance.event.location.entity_creator
        )
        playlist.save()
