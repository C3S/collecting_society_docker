#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the creations
"""

from proteus import Model

from . import test_text

DEPENDS = [
    'release',
]


def generate(reclimit=0):

    # constants
    creations_per_release = reclimit or 3

    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')
    Release = Model.get('release')

    # entries
    artist_releases = Release.find([
        ('claim_state', '!=', 'unclaimed'),
        ('type', '=', 'artist')
    ])
    foreign_artists = Artist.find([
        ('name', 'like', 'Foreign Original Artist%')])

    # create creations
    for i, release in enumerate(artist_releases):
        for j in range(1, creations_per_release + 1):
            number = i * creations_per_release + j
            artist = release.artists[0]
            creator = artist
            if creator.group:
                creator = creator.solo_artists[0]

            creation = Creation(
                title="Title of Song %s" % str(number).zfill(3),
                commit_state='commited',
                claim_state='claimed',
                entity_creator=creator.party,
                lyrics=test_text,
                artist=artist
            )
            creation.save()

    # create foreign creations for originals
    for i, artist in enumerate(foreign_artists):
        Creation(
            title="Foreign Original Song %s" % str(i).zfill(3),
            artist=artist,
            entity_creator=artist.entity_creator,
            entity_origin='indirect',
            commit_state='uncommited',
            claim_state='unclaimed'
        ).save()
