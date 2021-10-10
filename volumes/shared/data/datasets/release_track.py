#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the release tracks
"""

import datetime
import random

from proteus import Model

DEPENDS = [
    'creation',
    'license',
]


def generate(reclimit=0):

    # constants
    sampler_releases = reclimit or 1
    creations_per_sampler = reclimit or 5
    split_releases = reclimit or 1
    creations_per_split_artist = reclimit or 2

    # models
    Creation = Model.get('creation')
    Release = Model.get('release')
    License = Model.get('license')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])
    artist_releases = Release.find([
        ('claim_state', '!=', 'unclaimed'),
        ('type', '=', 'artist')
    ])
    sampler_releases = Release.find([
        ('claim_state', '!=', 'unclaimed'),
        ('type', '=', 'compilation')
    ])
    split_releases = Release.find([
        ('claim_state', '!=', 'unclaimed'),
        ('type', '=', 'split')
    ])

    # create artist release tracks
    creations_per_release = int(len(creations) / len(artist_releases))
    for i, release in enumerate(artist_releases):
        start = i * creations_per_release
        tracks = creations[start:start+creations_per_release]
        for j, creation in enumerate(tracks):
            licenses = License.find([])
            rc = release.tracks.new()
            rc.creation = creation
            rc.title = "Release Title of Song %s" % creation.title[:-3]
            rc.medium_number = 1
            rc.track_number = j
            rc.license = random.choice(licenses)
        release.save()

    # create sampler release tracks
    for release in sampler_releases:
        last_date = datetime.date(1, 1, 1)
        tracks = random.sample(creations, creations_per_sampler)
        for i, creation in enumerate(tracks):
            if creation.release.release_date > last_date:
                last_date = creation.release.release_date
            licenses = License.find([])
            rc = release.tracks.new()
            rc.creation = creation
            rc.title = "Renamed Song %s on a Compilation" % creation.title[:-3]
            rc.medium_number = 1
            rc.track_number = i
            rc.license = random.choice(licenses)
        if not release.confirmed_copies:
            release.production_date = last_date + datetime.timedelta(50)
            release.release_date = last_date + datetime.timedelta(100)
            release.online_release_date = last_date + datetime.timedelta(100)
        release.copyright_date = last_date + datetime.timedelta(80)
        release.save()

    # create split release tracks
    for release in split_releases:
        last_date = datetime.date(1, 1, 1)
        tracks = []
        for artist in release.artists:
            tracks += random.sample(
                artist.creations,
                min(creations_per_split_artist, len(artist.creations)))
        for i, creation in enumerate(tracks):
            if creation.release.release_date > last_date:
                last_date = creation.release.release_date
            licenses = License.find([])
            rc = release.tracks.new()
            rc.creation = creation
            rc.title = "Renamed Song %s on a Split" % creation.title[:-3]
            rc.medium_number = 1
            rc.track_number = i
            rc.license = random.choice(licenses)
        release.production_date = last_date + datetime.timedelta(50)
        release.copyright_date = last_date + datetime.timedelta(80)
        release.release_date = last_date + datetime.timedelta(100)
        release.online_release_date = last_date + datetime.timedelta(100)
        release.save()
