#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the devices messages for bars/webradios/podcasts
"""

import datetime

from proteus import Model

DEPENDS = [
    'device',
]


def generate(reclimit=0):

    # constants
    fingerprint_messages_per_space = reclimit or 60
    fingerprint_messages_per_channel = reclimit or 60
    usagereport_messages_per_episode = reclimit or 10

    # models
    Device = Model.get('device')

    # entries
    bar_devices = Device.find(['software_name', '=', 'Bar Tracker'])
    webradio_devices = Device.find(['software_name', '=', 'Webradio Tracker'])
    podcast_devices = Device.find(['software_name', '=', 'Podcast Reporter'])

    # content
    now = datetime.datetime.now()

    # create bar device messages (first space only)
    for device in bar_devices:
        for i in range(0, fingerprint_messages_per_space):
            message = device.messages.new()
            message.timestamp = now
            message.direction = 'incoming'
            message.category = 'fingerprint'
            message.context = device.assignments[0].assignment
        device.save()

    # create webradio device messages (first channel only)
    for device in webradio_devices:
        for i in range(0, fingerprint_messages_per_channel):
            message = device.messages.new()
            message.timestamp = now
            message.direction = 'incoming'
            message.category = 'fingerprint'
            message.context = device.assignments[0].assignment.resources[0]
        device.save()

    # create podcast device messages
    for device in podcast_devices:
        for episode in device.assignments[0].assignment.resources:
            for i in range(0, usagereport_messages_per_episode):
                message = device.messages.new()
                message.timestamp = now
                message.direction = 'incoming'
                message.category = 'usagereport'
                message.context = episode
            device.save()
