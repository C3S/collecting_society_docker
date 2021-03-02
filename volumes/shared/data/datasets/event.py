#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the events
"""

import random
import datetime
import decimal

from proteus import Model

DEPENDS = [
    'location',
]


def generate(reclimit=0):

    # constants
    events_per_location_space = reclimit or 3
    performances_per_event = reclimit or 3

    # models
    Event = Model.get('event')
    Location = Model.get('location')

    # entries
    locations = Location.find(['name', 'like', '%Performance%'])

    # content
    now = datetime.datetime.now()
    attendants_choices = [10, 100, 500, 1000, 5000, 10000]
    expenses_choices = [0, 50, 100, 1000]

    # create events
    for i, location in enumerate(locations):
        for j in range(1, events_per_location_space + 1):
            number = i * events_per_location_space + j
            date = now - datetime.timedelta(days=random.randint(-30, 30))
            attendants = random.choice(attendants_choices)
            event = Event(
                name='Event %s' % str(number).zfill(3),
                description='The %s. event' % str(number).zfill(3),
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
                    performances_per_event * random.choice(expenses_choices)
                ),
                estimated_expenses_production=decimal.Decimal(
                    performances_per_event * random.randint(100, 1000)
                )
            )
            event.save()
