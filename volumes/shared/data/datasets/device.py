#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create and assign the devices
"""

import datetime

from proteus import Model

DEPENDS = [
    'location_space',
]


def generate(reclimit=0):

    # models
    Location = Model.get('location')
    Device = Model.get('device')
    DeviceAssignment = Model.get('device.assignment')

    # entries
    bar_locations = Location.find(['name', 'like', '%Bar%'])

    # content
    now = datetime.datetime.now()

    # create devices for location spaces
    for bar_location in bar_locations:

        # create device
        device = Device(
            web_user=bar_location.entity_creator.web_user,
            blocked=False,
            name='Raspberry PI',
            os_name='Raspbian',
            os_version='10',
            software_name='Tracker',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # create device assignment
        DeviceAssignment(
            device=device,
            assignment=bar_location.spaces[0],
            start=now
        ).save()
