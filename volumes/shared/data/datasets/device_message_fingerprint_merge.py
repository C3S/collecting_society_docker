#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Merge the fingerprints
"""

from proteus import Model, Wizard

DEPENDS = [
    'device_message_fingerprint',
]


def generate(reclimit=0):

    # models
    LocationSpace = Model.get('location.space')
    WebsiteResource = Model.get('website.resource')

    # entries
    spaces = LocationSpace.find(['messages.category', '=', 'fingerprint'])
    resources = WebsiteResource.find(['messages.category', '=', 'fingerprint'])

    # merge fingerprints for location spaces
    for space in spaces:
        wizard = Wizard('device.message.fingerprint.merge')
        wizard.form.context = space
        wizard.form.start = space.fingerprints[0].timestamp
        wizard.form.end = space.fingerprints[-1].timestamp
        wizard.execute('select')
        wizard.execute('merge')

    # merge fingerprints for website resources
    for resource in resources:
        wizard = Wizard('device.message.fingerprint.merge')
        wizard.form.context = resource
        wizard.form.start = resource.fingerprints[0].timestamp
        wizard.form.end = resource.fingerprints[-1].timestamp
        wizard.execute('select')
        wizard.execute('merge')
