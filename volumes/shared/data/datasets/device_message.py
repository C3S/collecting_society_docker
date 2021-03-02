#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the devices messages
"""

import datetime

from proteus import Model

DEPENDS = [
    'device',
]


def generate(reclimit=0):

    # constants
    fingerprint_messages_per_device = reclimit or 60*3

    # models
    Device = Model.get('device')

    # entries
    devices = Device.find([])

    # content
    now = datetime.datetime.now()

    # create device messages
    for device in devices:
        for i in range(0, fingerprint_messages_per_device):
            message = device.messages.new()
            message.timestamp = now
            message.direction = 'incoming'
            message.category = 'fingerprint'
            message.context = device.assignments[0].assignment
        device.save()
