#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create and assign the devices for bars/webradios/podcasts/dsps
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
    podcast_websites = Website.find(['category.code', '=', 'P'])
    dsp_websites = Website.find(['category.code', '=', 'D'])

    # content
    now = datetime.datetime.now()

    # create devices for location spaces (first space only)
    for location in bar_locations:

        # create device
        device = Device(
            web_user=location.entity_creator.web_user,
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
            assignment=location.spaces[0],
            start=now
        ).save()

    # create devices for radio website channels (first channel only)
    for website in radio_websites:

        # create device
        device = Device(
            web_user=website.party.web_user,
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
            assignment=website,
            start=now
        ).save()

    # create devices for podcast website channels
    for website in podcast_websites:

        # create device
        device = Device(
            web_user=website.party.web_user,
            blocked=False,
            name='Podcast Reporter',
            software_name='Podcast Reporter',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # create device assignment
        DeviceAssignment(
            device=device,
            assignment=website,
            start=now
        ).save()

    # create devices for dsp website ugc
    for website in dsp_websites:

        # create device
        device = Device(
            web_user=website.party.web_user,
            blocked=False,
            name='DSP Reporter',
            software_name='DSP Reporter',
            software_version='1.0.0',
            software_vendor='C3S'
        )
        device.save()

        # create device assignment
        DeviceAssignment(
            device=device,
            assignment=website,
            start=now
        ).save()
