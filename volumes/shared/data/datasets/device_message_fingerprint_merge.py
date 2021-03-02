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

    # entries
    spaces = LocationSpace.find(['messages.category', '=', 'fingerprint'])

    # merge fingerprints
    for space in spaces:
        wizard = Wizard('device.message.fingerprint.merge')
        wizard.form.context = space
        wizard.form.start = space.fingerprints[0].timestamp
        wizard.form.end = space.fingerprints[-1].timestamp
        wizard.execute('select')
        wizard.execute('merge')
