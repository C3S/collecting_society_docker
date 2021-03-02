#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the artist/sampler/split/reproduction releases
"""

import datetime
import random

from proteus import Model

DEPENDS = [
    'artist',
    'publisher',
    'label',
    'genre',
    'style',
]


def generate(reclimit=0):

    # constants
    releases_per_artist = reclimit or 1
    genres_per_release = reclimit or 2
    styles_per_release = reclimit or 2
    release_cancellation_chance = reclimit and 1 or 0.3
    sampler_releases = reclimit or 1
    split_releases = reclimit or 1
    artists_per_split_release = reclimit or 2
    reproduction_releases_per_licensee = reclimit or 2

    # models
    WebUser = Model.get('web.user')
    Artist = Model.get('artist')
    Release = Model.get('release')
    Publisher = Model.get('publisher')
    Genre = Model.get('genre')
    Style = Model.get('style')
    Label = Model.get('label')
    Country = Model.get('country.country')

    # entries
    countries = Country.find([])
    artists = Artist.find([('claim_state', '!=', 'unclaimed')])
    licensees = WebUser.find([('roles.code', '=', 'licensee')])

    # content
    now = datetime.datetime.now()

    # create artist releases
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

    # create sampler releases
    for i in range(1, sampler_releases + 1):
        number = i
        solos = Artist.find([
            ('claim_state', '!=', 'unclaimed'),
            ('group', '=', False)])
        labels = Label.find([])
        genres = Genre.find([])
        styles = Style.find([])
        publishers = Publisher.find([])
        creator = random.choice(solos)

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

    # create split releases
    for i in range(1, split_releases + 1):
        number = i
        artists = Artist.find([('claim_state', '!=', 'unclaimed')])
        labels = Label.find([])
        genres = Genre.find([])
        styles = Style.find([])
        publishers = Publisher.find([])
        splits = random.sample(artists, artists_per_split_release)
        creator = splits[0]
        if creator.group:
            creator = creator.solo_artists[0]

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
            label_catalog_number=str(random.randint(10000, 99999)),
            publisher=random.choice(publishers)
        )
        release.artists.extend(splits)
        release.save()

    # create reproduction releases
    for i, licensee in enumerate(licensees):
        for j in range(1, reproduction_releases_per_licensee + 1):
            number = i * reproduction_releases_per_licensee + j
            artists = Artist.find([('claim_state', '!=', 'unclaimed')])
            labels = Label.find([])
            genres = Genre.find([])
            styles = Style.find([])
            publishers = Publisher.find([])
            splits = random.sample(artists, artists_per_split_release)
            creator = splits[0]
            if creator.group:
                creator = creator.solo_artists[0]
            production_date = now + datetime.timedelta(
                days=random.randint(30, 90)
            )
            release_date = production_date + datetime.timedelta(
                days=random.randint(30, 120)
            )
            release = Release(
                type="compilation",
                entity_creator=licensee.party,
                commit_state='commited',
                claim_state='claimed',
                title="Reproduction Release %s" % str(number).zfill(3),
                genres=random.sample(genres, min(
                    genres_per_release, len(genres))),
                styles=random.sample(styles, min(
                    styles_per_release, len(styles))),
                warning='WARNING: This is testdata!',
                copyright_date=datetime.date(
                    random.randint(1800, 2019),
                    random.randint(1, 12),
                    random.randint(1, 28)
                ),
                production_date=production_date,
                release_date=release_date,
                online_release_date=release_date,
                distribution_territory=random.choice(countries).code,
                label=random.choice(labels),
                label_catalog_number=str(random.randint(10000, 99999)),
                publisher=random.choice(publishers),
                confirmed_copies=random.choice([100, 1000, 10000, 100000])
            )
            release.artists.extend(splits)
            release.save()
