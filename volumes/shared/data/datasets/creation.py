#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create creations
"""

from proteus import  Model

import datetime
import random
import string

DEPENDS = [
    'artist',
    'release',
    'collecting_societies',
    'tariff',
    'license'
]


def generate(reclimit):

    # constants
    releases_per_artist = reclimit or 1
    creations_per_release = reclimit or 3
    test_text = '''Lorem ipsum dolor sit amet, consetetur diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren.\n\nLorem ipsum.\n\nSea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.'''

    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')
    Release = Model.get('release')
    License = Model.get('license')
    CreationTariffCategory = Model.get('creation-tariff_category')
    TariffCategory = Model.get('tariff_system.category')
    CollectingSociety = Model.get('collecting_society')

    artists = Artist.find([('claim_state', '!=', 'unclaimed')])
    releases = Release.find([('claim_state', '!=', 'unclaimed')])
    for i in range(1, len(releases) + 1):
        for j in range(1, creations_per_release + 1):
            number = (i - 1) * creations_per_release + j
            artist_number = divmod(i-1, releases_per_artist)[0]
            artist = artists[artist_number]
            creator = artist
            if creator.group:
                creator = creator.solo_artists[0]
            # creation
            creation = Creation(
                title="Title of Song %s" % str(number).zfill(3),
                commit_state='commited',
                claim_state='claimed',
                entity_creator=creator.party,
                lyrics=test_text,
                artist=artist
            )
            creation.save()

            # tariff categories
            css = CollectingSociety.find([(
                'represents_copyright', '=', True)])
            tariffcs = TariffCategory.find([])
            categories = random.sample(
                tariffcs, random.randint(1, len(tariffcs)))
            for category in categories:
                CreationTariffCategory(
                    creation=creation,
                    category=category,
                    collecting_society=random.choice(css)
                ).save()

            # release creation
            licenses = License.find([])
            cr = creation.releases.new()
            cr.creation=creation
            cr.release=releases[i-1]
            cr.title="Release Title of Song %s" % str(number).zfill(3)
            cr.medium_number=1
            cr.track_number=j
            cr.license=random.choice(licenses)
            cr.save()
            creation.save()
