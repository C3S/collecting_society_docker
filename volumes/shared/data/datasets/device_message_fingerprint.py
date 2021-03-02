#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the devices message fingerprints
"""

import datetime
import random
import string

from proteus import Model

DEPENDS = [
    'creation',
    'device_message',
]


def generate(reclimit=0):

    # models
    Creation = Model.get('creation')
    Device = Model.get('device')
    DeviceMessage = Model.get('device.message')
    DeviceMessageFingerprint = Model.get('device.message.fingerprint')

    # entries
    creations = Creation.find([])
    devices = Device.find([])

    # content
    chars_fingerprint = string.digits + string.letters

    # create device message fingerprints
    for device in devices:
        messages = DeviceMessage.find(['device', '=', device.id])
        timestamp = messages[0].timestamp - datetime.timedelta(days=1)
        creation = random.choice(creations)
        keep_creation = 0
        unknown_creation = False
        for message in messages:
            if not keep_creation:
                if unknown_creation:
                    creation = None
                else:
                    creation = random.choice(creations)
                keep_creation = random.randrange(0, 8)
                unknown_creation = random.random() > 0.6
            keep_creation -= 1
            timestamp = timestamp + datetime.timedelta(minutes=1)
            DeviceMessageFingerprint(
                message=[message],
                state='matched',
                matched_state=creation and 'success' or 'fail_score',
                matched_creation=creation,
                timestamp=timestamp,
                data=''.join(random.sample(
                    chars_fingerprint, len(chars_fingerprint))),
                algorithm='echoprint',
                version='1.0.0'
            ).save()
