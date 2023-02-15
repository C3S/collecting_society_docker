#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the devices messages for bars/webradios/podcasts/dsps
"""

import datetime

from proteus import Model

DEPENDS = [
    'device',
]


def generate(reclimit=0):

    # constants
    fingerprints_per_space = reclimit or 60
    fingerprints_per_channel = reclimit or 60
    usagereports_per_episode = reclimit or 10
    usagereports_per_dsp = reclimit or 10

    # models
    Device = Model.get('device')

    # entries
    bar_devices = Device.find(['software_name', '=', 'Bar Tracker'])
    webradio_devices = Device.find(['software_name', '=', 'Webradio Tracker'])
    podcast_devices = Device.find(['software_name', '=', 'Podcast Reporter'])
    dsp_devices = Device.find(['software_name', '=', 'DSP Reporter'])

    # content
    now = datetime.datetime.now()

    # create bar device messages (first space only)
    for device in bar_devices:
        for i in range(0, fingerprints_per_space):
            message = device.messages.new()
            message.timestamp = now
            message.direction = 'incoming'
            message.category = 'fingerprint'
            message.context = device.assignments[0].assignment
        device.save()

    # create webradio device messages (first channel only)
    for device in webradio_devices:
        for i in range(0, fingerprints_per_channel):
            resources = device.assignments[0].assignment.website_resources
            message = device.messages.new()
            message.timestamp = now
            message.direction = 'incoming'
            message.category = 'fingerprint'
            message.context = resources[0]
        device.save()

    # create podcast device messages
    for device in podcast_devices:
        resources = device.assignments[0].assignment.website_resources
        for episode in resources:
            for i in range(0, usagereports_per_episode):
                message = device.messages.new()
                message.timestamp = now
                message.direction = 'incoming'
                message.category = 'usagereport'
                message.context = episode
            device.save()

    # create dsp device messages
    for device in dsp_devices:
        for i in range(0, usagereports_per_dsp):
            resources = device.assignments[0].assignment.website_resources
            message = device.messages.new()
            message.timestamp = now
            message.direction = 'incoming'
            message.category = 'usagereport'
            message.context = resources[0]
        device.save()
