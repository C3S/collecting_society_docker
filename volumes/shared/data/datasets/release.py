#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create releases
"""

from proteus import  Model

import datetime
import random
import string

DEPENDS = [
    'artist',
    'publisher',
    'label',
    'genres_and_styles',
    'license',
    'web_user'
]


def generate(reclimit):

    # constants
    releases_per_artist = reclimit or 1
    genres_per_release = reclimit or 2
    styles_per_release = reclimit or 2
    release_cancellation_chance = reclimit and 1 or 0.3
    sampler_releases = reclimit or 1
    creations_per_sampler = reclimit or 5
    split_releases = reclimit or 1
    artists_per_split_release = reclimit or 2
    creations_per_split_artist = reclimit or 2

    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')
    Release = Model.get('release')
    ReleaseTrack = Model.get('release.track')
    Publisher = Model.get('publisher')
    Genre = Model.get('genre')
    Style = Model.get('style')
    Label = Model.get('label')
    Country = Model.get('country.country')
    WebUser = Model.get('web.user')
    License = Model.get('license')

    artists = Artist.find([('claim_state', '!=', 'unclaimed')])
    countries = Country.find([])
    for i in range(1, len(artists) + 1):
        for j in range(1, releases_per_artist + 1):
            number = (i - 1) * releases_per_artist + j
            owner = artists[i-1]
            creator = owner
            if creator.group:
                for solo in creator.solo_artists:
                    if solo.claim_state != 'unclaimed':
                        creator = solo
                        break
            publishers = Publisher.find([])
            labels = Label.find([])
            genres = Genre.find([])
            styles = Style.find([])
            release_date = datetime.date(
                random.randint(1800, 2019),
                random.randint(1, 12),
                random.randint(1, 28))
            isrc = ''.join(random.sample(string.ascii_uppercase, 3)) + \
                str(random.randint(1,999999999)).zfill(9)
            release = Release(
                type="artist",
                entity_creator=creator.party,
                commit_state='commited',
                claim_state='claimed',
                title="Release %s" % str(number).zfill(3),
                genres=random.sample(genres, min(
                    genres_per_release, len(genres))),
                styles=random.sample(styles, min(
                    styles_per_release, len(styles))),
                warning='WARNING: This is testdata!',
                copyright_date=release_date - datetime.timedelta(10),
                production_date=release_date - datetime.timedelta(30),
                release_date=release_date,
                distribution_territory=random.choice(countries).code,
                label=random.choice(labels),
                label_catalog_number=str(random.randint(10000, 99999)),
                publisher=random.choice(publishers)
            )
            if release.release_date.year >= 2000:
                release.online_release_date = release_date
            if random.random() < release_cancellation_chance:
                cancellation_date = release_date + datetime.timedelta(300)
                release.release_cancellation_date = cancellation_date
                if release.online_release_date:
                    release.online_cancellation_date = cancellation_date
            owner_artist, = Artist.find([('id', '=', owner.id)])
            release.artists.append(owner_artist)
            release.save()

        # Sampler Releases
    for i in range(1, sampler_releases + 1):
        number = i
        solos = Artist.find([
            ('claim_state', '!=', 'unclaimed'),
            ('group', '=', False)])
        labels = Label.find([])
        genres = Genre.find([])
        styles = Style.find([])
        isrc = ''.join(random.sample(string.ascii_uppercase, 3)) + \
            str(random.randint(1,999999999)).zfill(9)
        creations = Creation.find([('claim_state', '!=', 'unclaimed')])
        publishers = Publisher.find([])
        creator = random.choice(solos)
        web_user, = WebUser.find([('party.id', '=', creator.party.id)])

        # release
        release = Release(
            type="compilation",
            entity_creator=creator.party,
            commit_state='commited',
            claim_state='claimed',
            title="Sampler %s" % str(number).zfill(3),
            genres=random.sample(genres, min(
                genres_per_release, len(genres))),
            styles=random.sample(styles, min(
                styles_per_release, len(styles))),
            warning='WARNING: This is testdata!',
            distribution_territory=random.choice(countries).code,
            label=random.choice(labels),
            label_catalog_number=str(random.randint(10000, 99999)),
            publisher=random.choice(publishers)
        )
        release.save()

        # release creation
        tracks = random.sample(creations, creations_per_sampler)
        last_date = datetime.date(1,1,1)
        for i in range(0, len(tracks)):
            track = tracks[i]
            if track.release.release_date > last_date:
                last_date = track.release.release_date
            licenses = License.find([])
            rc = ReleaseTrack()
            rc.creation=track
            rc.release=release
            rc.title="Renamed Song %s on a Compilation" % str(
                number).zfill(3)
            rc.medium_number=1
            rc.track_number=i
            rc.license=random.choice(licenses)
            rc.save()

        release.production_date = last_date + datetime.timedelta(50)
        release.copyright_date = last_date + datetime.timedelta(80)
        release.release_date = last_date + datetime.timedelta(100)
        release.online_release_date = last_date + datetime.timedelta(100)
        release.save()

    # Split Releases
    for i in range(1, split_releases + 1):
        number = i
        artists = Artist.find([('claim_state', '!=', 'unclaimed')])
        labels = Label.find([])
        genres = Genre.find([])
        styles = Style.find([])
        isrc = ''.join(random.sample(string.ascii_uppercase, 3)) + \
            str(random.randint(1,999999999)).zfill(9)
        creations = Creation.find([('claim_state', '!=', 'unclaimed')])
        publishers = Publisher.find([])

        splits = random.sample(artists, artists_per_split_release)
        creator = splits[0]
        if creator.group:
            creator = creator.solo_artists[0]

        # release
        release = Release(
            type='split',
            entity_creator=creator.party,
            commit_state='commited',
            claim_state='claimed',
            title="Split Release %s" % str(number).zfill(3),
            genres=random.sample(genres, min(
                genres_per_release, len(genres))),
            styles=random.sample(styles, min(
                styles_per_release, len(styles))),
            warning='WARNING: This is testdata!',
            distribution_territory='Germany',
            label=random.choice(labels),
            label_catalog_number='12345',
            publisher=random.choice(publishers)
        )
        for split in splits:
            release.artists.append(split)
        release.save()

        # release creation
        last_date = datetime.date(1,1,1)
        for split in splits:
            tracks = random.sample(split.creations,
                min(creations_per_split_artist,len(split.creations)))
            for i in range(0, len(tracks)):
                track = tracks[i]
                if track.release.release_date > last_date:
                    last_date = track.release.release_date
                licenses = License.find([])
                rc = ReleaseTrack()
                rc.creation=track
                rc.release=release
                rc.title="Renamed Song %s on a Split Release" % str(
                    number).zfill(3)
                rc.medium_number=1
                rc.track_number=i
                rc.license=random.choice(licenses)
                rc.save()

        release.production_date = last_date + datetime.timedelta(50)
        release.copyright_date = last_date + datetime.timedelta(80)
        release.release_date = last_date + datetime.timedelta(100)
        release.online_release_date = last_date + datetime.timedelta(100)
        release.save()
