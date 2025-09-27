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
from .utilisation_allocation_collect import repeats_per_distribution_received

DEPENDS = [
    'location',
]


def generate(reclimit=0):

    # constants
    events_per_location = reclimit or 3
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

    number = 0

    # create events
    for state in ['estimated', 'confirmed', 'finalized', 'invoiced',
                  'posted', 'paid', 'distributed']:
        for playlist in [False, True]:
            for i, location in enumerate(locations):
                for j in range(1, events_per_location + 1):
                    tags = [f"{state}"]
                    if not playlist:
                        if state == 'estimated':
                            continue
                        tags.append("noplaylist")
                    number += 1
                    date_min = -60
                    date_max = -1
                    if state == 'estimated':
                        # half past, half future
                        if number % 2:
                            tags.append("past")
                            date_min = -30
                            date_max = -1
                        else:
                            tags.append("future")
                            date_min = 1
                            date_max = 30
                    date = now + datetime.timedelta(
                        days=random.randint(date_min, date_max))
                    attendants = random.choice(attendants_choices)
                    name = 'Event %s | %s' % (
                        str(number).zfill(3), " ".join(tags))
                    event = Event(
                        name=name,
                        description='The %s. event' % str(number).zfill(3),
                        location=location,
                        estimated_start=date,
                        estimated_end=date + datetime.timedelta(
                            hours=performances_per_event
                        ),
                        estimated_attendants=attendants,
                        estimated_max_attendants=attendants * 2,
                        estimated_max_admission=decimal.Decimal(
                            random.randint(0, 20)
                        ),
                        estimated_turnover_tickets=decimal.Decimal(
                            attendants * random.randint(0, 20)
                        ),
                        estimated_turnover_benefit=decimal.Decimal(
                            attendants * random.randint(1, 5)
                        ),
                        estimated_expenses_musicians=decimal.Decimal(
                            performances_per_event
                            * random.choice(expenses_choices)
                        ),
                        estimated_expenses_production=decimal.Decimal(
                            performances_per_event
                            * random.randint(100, 1000)
                        )
                    )
                    event.save()

    # create events in received distributions
    for batch in range(1, repeats_per_distribution_received + 1):
        for playlist in [False, True]:
            for i, location in enumerate(locations):
                for j in range(1, events_per_location + 1):
                    number += 1
                    date = now + datetime.timedelta(
                        days=random.randint(-60, -1))
                    attendants = random.choice(attendants_choices)
                    tags = ["received"]
                    if not playlist:
                        tags.append("noplaylist")
                    name = 'Event %s | %s' % (
                        str(number).zfill(3), " ".join(tags))
                    event = Event(
                        name=name,
                        description='The %s. event' % str(number).zfill(3),
                        location=location,
                        estimated_start=date,
                        estimated_end=date + datetime.timedelta(
                            hours=performances_per_event
                        ),
                        estimated_attendants=attendants,
                        estimated_max_attendants=attendants * 2,
                        estimated_max_admission=decimal.Decimal(
                            random.randint(0, 20)
                        ),
                        estimated_turnover_tickets=decimal.Decimal(
                            attendants * random.randint(0, 20)
                        ),
                        estimated_turnover_benefit=decimal.Decimal(
                            attendants * random.randint(1, 5)
                        ),
                        estimated_expenses_musicians=decimal.Decimal(
                            performances_per_event
                            * random.choice(expenses_choices)
                        ),
                        estimated_expenses_production=decimal.Decimal(
                            performances_per_event
                            * random.randint(100, 1000)
                        )
                    )
                    event.save()
