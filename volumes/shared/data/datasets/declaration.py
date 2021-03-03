#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the playing/life/reproduction/online declarations
"""

import datetime
import random

from proteus import Model

DEPENDS = [
    'tariff',
    'location',
    'event',
    'release',
    'website',
]


def generate(reclimit=0):

    # models
    Tariff = Model.get('tariff_system.tariff')
    Location = Model.get('location')
    Declaration = Model.get('declaration')
    Event = Model.get('event')
    Release = Model.get('release')
    Website = Model.get('website')

    # entries
    locations = Location.find([])
    tariff_playing = Tariff.find([('category.code', '=', 'P')])[-1]
    tariff_live = Tariff.find([('category.code', '=', 'L')])[-1]
    tariff_reproduction = Tariff.find([('category.code', '=', 'C')])[-1]
    tariff_online = Tariff.find([('category.code', '=', 'O')])[-1]
    events = Event.find([])
    releases = Release.find(['confirmed_copies', '>', 0])
    websites = Website.find([])

    # content
    now = datetime.datetime.now()
    periods = Declaration._fields['period']['selection']
    periods = [k for k, _ in periods if k]

    # create declarations for tariff playing
    for location in locations:
        Declaration(
            licensee=location.party,
            state='created',
            creation_time=now,
            template=False,
            period=random.choice(periods),
            tariff=tariff_playing,
            context=location
        ).save()

    # create declarations for tariff live
    for event in events:
        Declaration(
            licensee=event.location.entity_creator,
            state='created',
            creation_time=event.estimated_start - datetime.timedelta(
                days=random.randint(10, 30)
            ),
            template=False,
            period='onetime',
            tariff=tariff_live,
            context=event
        ).save()

    # create declarations for tariff reproduction
    for release in releases:
        Declaration(
            licensee=release.entity_creator,
            state='created',
            creation_time=now - datetime.timedelta(
                days=random.randint(10, 30)
            ),
            template=False,
            period='onetime',
            tariff=tariff_reproduction,
            context=release
        ).save()

    # create declarations for tariff online
    for website in websites:
        Declaration(
            licensee=website.party,
            state='created',
            creation_time=now,
            template=False,
            period=random.choice(periods),
            tariff=tariff_online,
            context=website
        ).save()
