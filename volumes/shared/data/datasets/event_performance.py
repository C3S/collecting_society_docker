#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the performances
"""

import random
import datetime

from proteus import Model

DEPENDS = [
    'artist',
    'event',
]


def generate(reclimit=0):

    # constants
    performances_per_event = reclimit or 3

    # models
    Artist = Model.get('artist')
    Event = Model.get('event')

    # entries
    artists = Artist.find([])
    events = Event.find([])

    # create performances
    for event in events:
        for j in range(1, performances_per_event + 1):
            artist = random.choice(artists)
            performance = event.performances.new()
            performance.event = event
            performance.artist = artist
            performance.start = event.estimated_start + datetime.timedelta(
                hours=j
            )
            performance.end = event.estimated_start + datetime.timedelta(
                hours=j + 1
            )
        event.save()
