#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the opening hours for locations
"""

import datetime
import random

from proteus import Model

DEPENDS = [
    'location',
]


def generate(reclimit=0):

    # models
    Location = Model.get('location')
    LocationIndicatorsPeriod = Model.get('location.indicators.period')

    # entries
    locations = Location.find([])

    # content
    weekdays = LocationIndicatorsPeriod._fields['start_weekday']['selection']
    weekdays = [k for k, _ in weekdays if k]

    # create periods
    for location in locations:
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
