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
    licensee_playing_locations = reclimit or 1
    licensee_live_locations = reclimit or 1

    # models
    Country = Model.get('country.country')
    Party = Model.get('party.party')
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

    # create locations for playing / bar
    for i, licensee in enumerate(licensees):
        for j in range(1, licensee_playing_locations + 1):
            number = i * licensee_playing_locations + j

            # create party
            party = Party(name="Location Bar %s" % str(number).zfill(3))
            _ = party.addresses.pop()
            party.addresses.new(
                street='Teststreet %s' % str(number),
                zip=str(10000+number).zfill(5),
                city='Testcity',
                country=germany
            )
            party.save()

            # create location
            location = Location(
                name="Location Bar %s" % str(number).zfill(3),
                category=random.choice(categories_playing),
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

    # create locations for live / performance
    for i, licensee in enumerate(licensees):
        for j in range(1, licensee_live_locations + 1):
            number = i * licensee_live_locations + j

            # create party
            party = Party(
                name="Location Performance %s" % str(number).zfill(3))
            _ = party.addresses.pop()
            party.addresses.new(
                street='Teststreet %s' % str(number),
                zip=str(10000+number).zfill(5),
                city='Testcity',
                country=germany
            )
            party.save()

            # create location
            location = Location(
                name="Location Performance %s" % str(number).zfill(3),
                category=random.choice(categories_live),
                party=party,
                public=True,
                latitude=random.random()*180-90,
                longitude=random.random()*360-180,
                entity_creator=licensee.party
            )
            location.save()
