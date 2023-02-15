#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the harddisks
"""

import uuid
from itertools import cycle

from proteus import Model

DEPENDS = [
    'harddisk_label',
]


def generate(reclimit=0):

    # constants
    harddisks_per_harddisklabel = reclimit or 2

    # models
    Harddisk = Model.get('harddisk')
    HarddiskLabel = Model.get('harddisk.label')
    Storehouse = Model.get('storehouse')

    # entries
    storehouses = Storehouse.find([])
    harddisk_labels = HarddiskLabel.find([])

    # create harddisks
    hosts = {}
    for storehouse in storehouses:
        hosts[storehouse] = str(uuid.uuid4())
    for storehouse, harddisk_label in zip(cycle(storehouses), harddisk_labels):
        for i in range(1, harddisks_per_harddisklabel + 1):
            harddisk = Harddisk(
                label=harddisk_label,
                version=1,
                storehouse=storehouse,
                location='SomeMachine',
                closed=False,
                raid_type="1",
                raid_number=str(i),
                raid_total=str(harddisks_per_harddisklabel),
                uuid_host=hosts[storehouse],
                uuid_harddisk=str(uuid.uuid4()),
                user=storehouse.user,
                online=True,
                state='in_use'
            )
            harddisk.save()
