#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the locations: playing/bar, live/performance
"""

import decimal
import random

from proteus import Model

DEPENDS = [
    'web_user',
    'location_category',
]


def generate(reclimit=0):

    # constants
    playing_locations_per_licensee = reclimit or 2
    live_locations_per_licensee = reclimit or 2

    # models
    Country = Model.get('country.country')
    Party = Model.get('party.party')
    Company = Model.get('company.company')
    WebUser = Model.get('web.user')
    LocationCategory = Model.get('location.category')
    Location = Model.get('location')

    # entries
    germany, = Country.find([('code', '=', 'DE')])
    licensees = WebUser.find([('roles.code', '=', 'licensee')])
    categories_playing = LocationCategory.find(
        [('code', 'in', ['B', 'N'])])
    categories_live = LocationCategory.find(
        [('code', 'in', ['B', 'N', 'O', 'M'])])
    company, = Company.find([(
        'party.name', '=',
        'C3S SCE'
    )])

    # create locations for playing / bar
    for i, licensee in enumerate(licensees):
        for j in range(1, playing_locations_per_licensee + 1):
            number = i * playing_locations_per_licensee + j

            # create party
            party = Party(name="Location Bar %s Owner" % str(number).zfill(3))
            _ = party.addresses.pop()
            street = 'Teststreet %s' % str(number)
            postal_code = str(10000+number).zfill(5)
            city = 'Testcity'
            country = germany
            party.addresses.new(
                street=street,
                postal_code=postal_code,
                city=city,
                country=country
            )
            party.save()

            # create location
            location = Location(
                name="Location Bar %s" % str(number).zfill(3),
                category=random.choice(categories_playing),
                party=party,
                public=True,
                street=street,
                postal_code=postal_code,
                city=city,
                country=country,
                latitude=random.random()*180-90,
                longitude=random.random()*360-180,
                estimated_turnover_gastronomy=decimal.Decimal(
                    random.randint(1000, 100000)
                ),
                entity_creator=licensee.party
            )
            location.save()

    # create locations for live / performance
    for i, licensee in enumerate(licensees):
        for j in range(1, live_locations_per_licensee + 1):
            number = i * live_locations_per_licensee + j

            # create party
            party = Party(
                name="Location Performance %s" % str(number).zfill(3))
            _ = party.addresses.pop()
            street = 'Teststreet %s' % str(number)
            postal_code = str(10000+number).zfill(5)
            city = 'Testcity'
            country = germany
            party.addresses.new(
                street=street,
                postal_code=postal_code,
                city=city,
                country=country
            )
            party.save()

            # create location
            location = Location(
                name="Location Performance %s" % str(number).zfill(3),
                category=random.choice(categories_live),
                party=party,
                public=True,
                street=street,
                postal_code=postal_code,
                city=city,
                country=country,
                latitude=random.random()*180-90,
                longitude=random.random()*360-180,
                entity_creator=licensee.party
            )
            location.save()
