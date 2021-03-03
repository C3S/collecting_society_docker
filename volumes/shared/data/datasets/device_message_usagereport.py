#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the devices message usagereports
"""

import datetime
import random
import decimal

from proteus import Model

DEPENDS = [
    'device_message',
]


def generate(reclimit=0):

    # constants
    usagereport_messages_per_episode = reclimit or 10

    # models
    Device = Model.get('device')
    DeviceMessage = Model.get('device.message')
    DeviceMessageUsagereport = Model.get('device.message.usagereport')

    # entries
    devices = Device.find(['software_name', 'like', '%Reporter'])

    # content
    now = datetime.datetime.now()

    # create usagereports for podcast episodes
    for device in devices:
        for episode in device.assignments[0].assignment.resources:
            timestamp = now - datetime.timedelta(
                days=7*usagereport_messages_per_episode)
            messages = DeviceMessage.find([
                ('device', '=', device.id),
                ('context', '=', "website.resource,%s" % episode.id),
                ('category', '=', 'usagereport')])
            for message in messages:
                timestamp = timestamp + datetime.timedelta(days=7)
                streams = random.randint(10, 1000000)
                downloads = int(streams / 100)
                DeviceMessageUsagereport(
                    message=[message],
                    state='created',
                    timestamp=timestamp,
                    reported_streams=streams,
                    reported_downloads=downloads,
                    reported_turnover_ads=decimal.Decimal(
                        streams / random.randint(100, 10000)
                    ),
                    reported_turnover_sale=decimal.Decimal(
                        downloads / random.randint(1, 100)
                    )
                ).save()
