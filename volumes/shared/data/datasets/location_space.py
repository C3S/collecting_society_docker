#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the location spaces: playing/bar, live/performance
"""

import random

from proteus import Model

DEPENDS = [
    'location_space_category',
    'location',
]


def generate(reclimit=0):

    # constants
    location_spaces_per_location = reclimit or 2

    # models
    LocationSpaceCategory = Model.get('location.space.category')
    LocationSpace = Model.get('location.space')
    Location = Model.get('location')

    # entries
    bar_categories = LocationSpaceCategory.find([])
    bar_locations = Location.find(['name', 'like', '%Bar%'])
    performance_category, = LocationSpaceCategory.find([('code', '=', 'C')])
    performance_locations = Location.find(['name', 'like', '%Performance%'])

    # create location spaces for bars
    for bar_location in bar_locations:
        for category in random.sample(
                bar_categories, location_spaces_per_location):
            LocationSpace(
                location=bar_location,
                category=random.choice(bar_categories),
                estimated_size=random.randint(10, 100)
            ).save()

    # create location spaces for performances
    for performance_location in performance_locations:
        for i in range(0, location_spaces_per_location):
            LocationSpace(
                location=performance_location,
                category=performance_category,
                estimated_size=random.randint(10, 100)
            ).save()
