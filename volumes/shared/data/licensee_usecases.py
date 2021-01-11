#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the licensee usecases
"""

import string
import random
import datetime
import decimal

from proteus import Model, Wizard

DEPENDS = [
    'artist',
    'label',
    'genre',
    'style',
    'license',
    'publisher',
    'location',
    'website',
    'web_user',
    'tariff',
    'creation',
]


def generate(reclimit=0):

    # constants
    licensee_playing_bars = reclimit or 1
    fingerprint_messages_per_device = reclimit or 60*3
    usagereport_messages_per_device = reclimit or 10
    licensee_live_events = reclimit or 3
    performances_per_event = reclimit or 3
    items_per_performance_playlist = reclimit or 5
    licensee_reproduction_releases = reclimit or 3
    creations_per_reproduction_release = reclimit or 10
    channels_per_webradio = reclimit or 3
    episodes_per_podcast = reclimit or 3
    originals_per_episode = reclimit or 5
    genres_per_release = reclimit or 2
    styles_per_release = reclimit or 2
    weekdays = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday',
    ]
    declaration_periods = [
        'monthly',
        'quarterly',
        'yearly',
    ]
    # models
    Artist = Model.get('artist')
    Creation = Model.get('creation')
    Release = Model.get('release')
    ReleaseTrack = Model.get('release.track')
    Party = Model.get('party.party')
    Location = Model.get('location')
    LocationCategory = Model.get('location.category')
    LocationSpaceCategory = Model.get('location.space.category')
    Event = Model.get('event')
    EventPerformance = Model.get('event.performance')
    Tariff = Model.get('tariff_system.tariff')
    WebUser = Model.get('web.user')
    Device = Model.get('device')
    DeviceAssignment = Model.get('device.assignment')
    DeviceMessage = Model.get('device.message')
    DeviceMessageFingerprint = Model.get('device.message.fingerprint')
    DeviceMessageUsagereport = Model.get('device.message.usagereport')
    LocationIndicatorsPeriod = Model.get('location.indicators.period')
    Declaration = Model.get('declaration')
    Website = Model.get('website')
    WebsiteCategory = Model.get('website.category')
    WebsiteResource = Model.get('website.resource')
    WebsiteResourceCategory = Model.get('website.resource.category')
    Country = Model.get('country.country')
    LocationSpace = Model.get('location.space')
    LocationSpaceCategory = Model.get('location.space.category')
    ArtistPlaylist = Model.get('artist.playlist')
    ArtistPlaylistItem = Model.get('artist.playlist.item')
    Genre = Model.get('genre')
    Style = Model.get('style')
    Label = Model.get('label')
    License = Model.get('license')
    Publisher = Model.get('publisher')

    # commonly used values
    now = datetime.datetime.now()
    germany, = Country.find([('code', '=', 'DE')])
    countries = Country.find([])
    publishers = Publisher.find([])

    # Licensee Usecase: Playing / Bar
    licensees = WebUser.find(
        [('roles.code', '=', 'licensee')])
    location_categories = LocationCategory.find(
        [('code', 'in', ['B', 'N'])])
    location_space_categories = LocationSpaceCategory.find([])
    tariff_playing = Tariff.find(
        [('category.name', '=', 'Playing')])[-1]
    creations = Creation.find([])
    chars_fingerprint = string.digits + string.letters
    for i in range(0, len(licensees)):
        licensee = licensees[i - 1]

        for j in range(1, licensee_playing_bars + 1):
            number = i * licensee_playing_bars + j

            party = Party(name="Location Bar %s" % str(number).zfill(3))
            _ = party.addresses.pop()
            # party_address =
            party.addresses.new(
                street='Teststreet %s' % str(number),
                zip=str(10000+number).zfill(5),
                city='Testcity',
                country=germany
            )
            party.save()

            # location
            location = Location(
                name="Location Bar %s" % str(number).zfill(3),
                category=random.choice(location_categories),
                party=party,
                public=True,
                latitude=random.random()*180-90,
                longitude=random.random()*360-180,
                estimated_turnover_gastronomy=decimal.Decimal(
                    random.randint(1000, 100000)
                ),
                entity_creator=licensee.party
            )
            location.save()

            # opening hours
            for d in range(0, len(weekdays)):
                if random.random() < 0.5:
                    continue
                LocationIndicatorsPeriod(
                    location_indicators=location.estimated_indicators,
                    start_weekday=weekdays[d],
                    start_time=datetime.time(
                        hour=random.choice(range(0, 17)),
                        minute=random.choice([0, 30])
                    ),
                    end_weekday=weekdays[d],
                    end_time=datetime.time(
                        hour=random.choice(range(17, 24)),
                        minute=random.choice([0, 30])
                    )
                ).save()

            # location spaces
            for lsc in range(0, len(location_space_categories)):
                category = location_space_categories[lsc]
                if lsc and random.random() > 0.5:
                    continue
                LocationSpace(
                    location=location,
                    category=category,
                    estimated_size=random.randint(10, 100)
                ).save()

            # declaration
            Declaration(
                licensee=licensee.party,
                state='created',
                creation_time=now,
                template=False,
                period=random.choice(declaration_periods),
                tariff=tariff_playing,
                context=location
            ).save()

            # device
            device = Device(
                web_user=licensee,
                blocked=False,
                name='Raspberry PI',
                os_name='Raspbian',
                os_version='10',
                software_name='Tracker',
                software_version='1.0.0',
                software_vendor='C3S'
            )
            device.save()

            # device assignment
            DeviceAssignment(
                device=device,
                assignment=location.spaces[0],
                start=now
            ).save()

            # device messages
            timestamp = now - datetime.timedelta(days=1)
            creation = random.choice(creations)
            keep_creation = 0
            unknown_creation = False

            for i in range(0, fingerprint_messages_per_device):

                # device message
                message = DeviceMessage(
                    device=device,
                    timestamp=now,
                    direction='incoming',
                    category='fingerprint',
                    context=location.spaces[0]
                )
                message.save()

                # device message fingerprint
                if not keep_creation:
                    if unknown_creation:
                        creation = None
                    else:
                        creation = random.choice(creations)
                    keep_creation = random.randrange(0, 8)
                    unknown_creation = random.random() > 0.6
                keep_creation -= 1
                timestamp = timestamp + datetime.timedelta(minutes=1)
                DeviceMessageFingerprint(
                    message=[message],
                    state='matched',
                    matched_state=creation and 'success' or 'fail_score',
                    matched_creation=creation,
                    timestamp=timestamp,
                    data=''.join(random.sample(
                        chars_fingerprint, len(chars_fingerprint))),
                    algorithm='echoprint',
                    version='1.0.0'
                ).save()
    # Merge Fingerprints::
    contexts = LocationSpace.find(
        ['messages.category', '=', 'fingerprint'])
    for context in contexts[:-1]:
        wizard = Wizard('device.message.fingerprint.merge')
        wizard.form.context = context
        wizard.form.start = context.fingerprints[0].timestamp
        wizard.form.end = context.fingerprints[-1].timestamp
        wizard.execute('select')
        wizard.execute('merge')
    # Licensee Usecase: Life / Performances
    licensees = WebUser.find(['roles.code', '=', 'licensee'])
    location_categories = LocationCategory.find(
        [('code', 'in', ['B', 'N', 'O', 'M'])])
    location_space_category_concert, = LocationSpaceCategory.find(
        [('code', '=', 'C')])
    tariff_live = Tariff.find(
        [('category.name', '=', 'Live')])[-1]
    artists = Artist.find([])
    location_number = 1
    event_number = 1
    for licensee in licensees:

        party = Party(name="Location Performance %s" %
                      str(location_number).zfill(3))
        _ = party.addresses.pop()
        # party_address =
        party.addresses.new(
            street='Teststreet %s' % str(location_number),
            zip=str(10000+location_number).zfill(5),
            city='Testcity',
            country=germany
        )
        party.save()

        # location
        location = Location(
            name="Location Performance %s" % str(location_number).zfill(3),
            category=random.choice(location_categories),
            party=party,
            public=True,
            latitude=random.random()*180-90,
            longitude=random.random()*360-180,
            entity_creator=licensee.party
        )
        location.save()
        location_number += 1

        # location spaces
        LocationSpace(
            location=location,
            category=location_space_category_concert,
            estimated_size=random.randint(10, 100)
        ).save()

        # event
        for i in range(0, licensee_live_events):

            date = now - datetime.timedelta(days=random.randint(-30, 30))
            attendants = random.choice(
                [10, 100, 500, 1000, 5000, 10000]
            )
            event = Event(
                name='Event %s' % str(event_number).zfill(3),
                description='The %s. event' % str(event_number).zfill(3),
                location=location,
                estimated_start=date,
                estimated_end=date + datetime.timedelta(
                    hours=performances_per_event
                ),
                estimated_attendants=attendants,
                estimated_turnover_tickets=decimal.Decimal(
                    attendants * random.randint(0, 20)
                ),
                estimated_turnover_benefit=decimal.Decimal(
                    attendants * random.randint(1, 5)
                ),
                estimated_expenses_musicians=decimal.Decimal(
                    performances_per_event * random.choice(
                        [0, 50, 100, 1000]
                    )
                ),
                estimated_expenses_production=decimal.Decimal(
                    performances_per_event * random.randint(100, 1000)
                )
            )
            event.save()
            event_number += 1

            # performances
            for j in range(0, performances_per_event):
                artist = random.choice(artists)

                # performance
                performance = EventPerformance(
                    event=event,
                    start=event.estimated_start + datetime.timedelta(
                        hours=j
                    ),
                    end=event.estimated_start + datetime.timedelta(
                        hours=j + 1
                    ),
                    artist=artist
                )
                performance.save()

                # playlist
                playlist = ArtistPlaylist(
                    artist=artist,
                    public=False,
                    template=False,
                    performance=[performance],
                    entity_origin='indirect',
                    entity_creator=licensee.party
                )
                playlist.save()

                # playlist items
                if artist.creations and random.random() > 0.1:
                    creation = random.choice(artist.creations)
                else:
                    creation = random.choice(creations)
                for k in range(1, items_per_performance_playlist + 1):
                    ArtistPlaylistItem(
                        playlist=playlist,
                        creation=creation,
                        position=k,
                        entity_origin='indirect',
                        entity_creator=licensee.party
                    ).save()

            # declaration
            Declaration(
                licensee=licensee.party,
                state='created',
                creation_time=date - datetime.timedelta(
                    days=random.randint(10, 30)
                ),
                template=False,
                period='onetime',
                tariff=tariff_live,
                context=event
            ).save()
    # Licensee Usecase: Reproduction / Release
    licensees = WebUser.find(['roles.code', '=', 'licensee'])
    tariff_reproduction = Tariff.find(
        [('category.name', '=', 'Reproduction')])[-1]
    release_number = 1
    for licensee in licensees:

        for i in range(0, licensee_reproduction_releases):

            # release
            artist = random.choice(artists)
            production_date = now + datetime.timedelta(
                days=random.randint(30, 90)
            )
            release_date = production_date + datetime.timedelta(
                days=random.randint(30, 120)
            )
            artists = Artist.find([])
            labels = Label.find([])
            genres = Genre.find([])
            styles = Style.find([])
            release = Release(
                type="artist",
                artists=[artist],
                entity_creator=licensee.party,
                commit_state='uncommited',
                claim_state='unclaimed',
                title="Reproduction Release %s" % str(
                    release_number).zfill(3),
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
            release.save()
            release_number += 1

            # release tracks
            creations = Creation.find([])
            tracks = random.sample(
                creations,
                min(creations_per_reproduction_release, len(creations))
            )
            for i, track in enumerate(tracks):
                rc = ReleaseTrack()
                rc.creation = track
                rc.release = release
                rc.title = creation.title  # TODO: creation variable unbound?
                rc.medium_number = 1
                rc.track_number = i + 1
                rc.license = random.choice(License.find([]))
                rc.save()

            # declaration
            Declaration(
                licensee=licensee.party,
                state='created',
                creation_time=now - datetime.timedelta(
                    days=random.randint(10, 30)
                ),
                template=False,
                period='onetime',
                tariff=tariff_reproduction,
                context=release
            ).save()
    # Licensee Usecase: Online / Webradio
    licensees = WebUser.find(['roles.code', '=', 'licensee'])
    creations = Creation.find([])
    tariff_online = Tariff.find(
        [('category.name', '=', 'Online')])[-1]
    website_category_webradio, = WebsiteCategory.find(
        [('name', '=', 'Webradio')])
    website_resource_category_channel, = WebsiteResourceCategory.find(
        [('name', '=', 'Channel')])
    webradio_number = 1
    channel_number = 1
    for licensee in licensees:

        # website
        website = Website(
            name='Webradio %s' % str(webradio_number).zfill(3),
            category=website_category_webradio,
            party=licensee.party,
            url='https://webradio%s.test' % str(webradio_number).zfill(3)
        )
        website.save()
        webradio_number += 1

        # website resources
        for i in range(0, channels_per_webradio):

            # website resource
            website_resource = WebsiteResource(
                website=website,
                name='Channel %s' % str(channel_number).zfill(3),
                category=website_resource_category_channel,
                url='https://channel%s.webradio%s.test' % (
                    str(channel_number).zfill(3),
                    str(webradio_number).zfill(3)
                )
            )
            website_resource.save()
            channel_number += 1

        # declaration
        Declaration(
            licensee=licensee.party,
            state='created',
            creation_time=now,
            template=False,
            period=random.choice(declaration_periods),
            tariff=tariff_online,
            context=website
        ).save()

        # device
        device = Device(
            web_user=licensee,
            blocked=False,
            name='Raspberry PI',
            os_name='Raspbian',
            os_version='10',
            software_name='Tracker',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # device assignment
        DeviceAssignment(
            device=device,
            assignment=website,
            start=now
        ).save()

        # device messages
        for channel in website.resources:

            timestamp = now - datetime.timedelta(days=1)
            creation = random.choice(creations)
            keep_creation = 0
            unknown_creation = False

            for i in range(0, fingerprint_messages_per_device):

                # device message
                message = DeviceMessage(
                    device=device,
                    timestamp=now,
                    direction='incoming',
                    category='fingerprint',
                    context=channel
                )
                message.save()

                # device message fingerprint
                if not keep_creation:
                    if unknown_creation:
                        creation = None
                    else:
                        creation = random.choice(creations)
                    keep_creation = random.randrange(0, 8)
                    unknown_creation = random.random() > 0.6
                keep_creation -= 1
                timestamp = timestamp + datetime.timedelta(minutes=1)
                DeviceMessageFingerprint(
                    message=[message],
                    state='matched',
                    matched_state=creation and 'success' or 'fail_score',
                    matched_creation=creation,
                    timestamp=timestamp,
                    data=''.join(random.sample(
                        chars_fingerprint, len(chars_fingerprint))),
                    algorithm='echoprint',
                    version='1.0.0'
                ).save()
    # Merge Fingerprints
    contexts = WebsiteResource.find(
        ['messages.category', '=', 'fingerprint'])
    for context in contexts[:-1]:
        wizard = Wizard('device.message.fingerprint.merge')
        wizard.form.context = context
        wizard.form.start = context.fingerprints[0].timestamp
        wizard.form.end = context.fingerprints[-1].timestamp
        wizard.execute('select')
        wizard.execute('merge')
    # Licensee Usecase: Online / Podcast
    licensees = WebUser.find(['roles.code', '=', 'licensee'])
    tariff_online = Tariff.find(
        [('category.name', '=', 'Online')])[-1]
    website_category_podcast, = WebsiteCategory.find(
        [('name', '=', 'Podcast')])
    website_resource_category_episode, = WebsiteResourceCategory.find(
        [('name', '=', 'Episode')])
    podcast_number = 1
    episode_number = 1
    for licensee in licensees:

        # website
        website = Website(
            name='Podcast %s' % str(podcast_number).zfill(3),
            category=website_category_podcast,
            party=licensee.party,
            url='https://podcast%s.test' % str(podcast_number).zfill(3)
        )
        website.save()
        podcast_number += 1

        # website resources
        for i in range(0, episodes_per_podcast):

            # website resource
            website_resource = WebsiteResource(
                website=website,
                name='Episode %s' % str(episode_number).zfill(3),
                category=website_resource_category_episode,
                url='https://podcast%s.test/episode%s' % (
                    str(podcast_number).zfill(3),
                    str(episode_number).zfill(3)
                ),
                originals=random.sample(
                    Creation.find([]), originals_per_episode)
            )
            website_resource.save()
            episode_number += 1

        # declaration
        Declaration(
            licensee=licensee.party,
            state='created',
            creation_time=now,
            template=False,
            period=random.choice(declaration_periods),
            tariff=tariff_online,
            context=website
        ).save()

        # device
        device = Device(
            web_user=licensee,
            blocked=False,
            name='Podcast Reporter',
            software_name='Reporter',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # device assignment
        DeviceAssignment(
            device=device,
            assignment=website,
            start=now
        ).save()

        # device messages
        for episode in website.resources:
            timestamp = now - datetime.timedelta(
                days=7*usagereport_messages_per_device)
            for i in range(0, usagereport_messages_per_device):

                # device message
                message = DeviceMessage(
                    device=device,
                    timestamp=now,
                    direction='incoming',
                    category='usagereport',
                    context=episode
                )
                message.save()

                # device message usagereport
                timestamp = timestamp + datetime.timedelta(days=7)
                streams = random.randint(10, 1000000)
                downloads = int(streams / 100)
                DeviceMessageUsagereport(
                    message=[message],
                    state='created',
                    timestamp=timestamp,
                    reported_streams=streams,
                    reported_downloads=downloads,
                    reported_turnover_ads=decimal.Decimal(
                        streams / random.randint(100, 10000)
                    ),
                    reported_turnover_sale=decimal.Decimal(
                        downloads / random.randint(1, 100)
                    )
                ).save()
    # Licensee Usecase: Online / DSP
    licensees = WebUser.find(['roles.code', '=', 'licensee'])
    creations = Creation.find([])
    tariff_online = Tariff.find(
        [('category.name', '=', 'Online')])[-1]
    website_category_dsp, = WebsiteCategory.find(
        [('name', '=', 'DSP')])
    website_resource_category_ugc, = WebsiteResourceCategory.find(
        [('name', '=', 'User Generated Content')])
    dsp_number = 1
    ugc_number = 1
    for licensee in licensees:

        # website
        website = Website(
            name='DSP %s' % str(dsp_number).zfill(3),
            category=website_category_dsp,
            party=licensee.party,
            url='https://dsp%s.test' % str(dsp_number).zfill(3)
        )
        website.save()
        dsp_number += 1

        # website resource
        website_resource = WebsiteResource(
            website=website,
            name='UGC %s' % str(ugc_number).zfill(3),
            category=website_resource_category_ugc
        )
        website_resource.save()
        ugc_number += 1

        # declaration
        Declaration(
            licensee=licensee.party,
            state='created',
            creation_time=now,
            template=False,
            period=random.choice(declaration_periods),
            tariff=tariff_online,
            context=website
        ).save()

        # device
        device = Device(
            web_user=licensee,
            blocked=False,
            name='UGC Reporter',
            software_name='Reporter',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # device assignment
        DeviceAssignment(
            device=device,
            assignment=website,
            start=now
        ).save()

        # device messages
        timestamp = now - datetime.timedelta(
            days=7*usagereport_messages_per_device)
        for i in range(0, usagereport_messages_per_device):

            # device message
            message = DeviceMessage(
                device=device,
                timestamp=now,
                direction='incoming',
                category='usagereport',
                context=website_resource
            )
            message.save()

            # device message usagereport
            timestamp = timestamp + datetime.timedelta(days=7)
            streams = random.randint(10, 1000000)
            downloads = int(streams / 100)
            DeviceMessageUsagereport(
                message=[message],
                state='created',
                timestamp=timestamp,
                creation=random.choice(creations),
                reported_streams=streams,
                reported_downloads=downloads,
                reported_turnover_ads=decimal.Decimal(
                    streams / random.randint(100, 10000)
                ),
                reported_turnover_sale=decimal.Decimal(
                    downloads / random.randint(1, 100)
                )
            ).save()
