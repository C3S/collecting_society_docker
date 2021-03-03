#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create and assign the devices for bars/webradios
"""

import datetime

from proteus import Model

DEPENDS = [
    'location_space',
    'website_resource',
]


def generate(reclimit=0):

    # models
    Location = Model.get('location')
    Website = Model.get('website')
    Device = Model.get('device')
    DeviceAssignment = Model.get('device.assignment')

    # entries
    bar_locations = Location.find(['name', 'like', '%Bar%'])
    radio_websites = Website.find(['category.code', '=', 'R'])

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
            software_name='Bar Tracker',
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

    # create devices for radio website channels
    for radio_website in radio_websites:

        # create device
        device = Device(
            web_user=radio_website.party.web_user,
            blocked=False,
            name='Raspberry PI',
            os_name='Raspbian',
            os_version='10',
            software_name='Webradio Tracker',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # create device assignment
        DeviceAssignment(
            device=device,
            assignment=radio_website,
            start=now
        ).save()
