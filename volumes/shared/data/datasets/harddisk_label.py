#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the archiving objects
"""

from proteus import Model

DEPENDS = [
    'storehouse',
]


def generate(reclimit=0):

    # constants
    harddisklabels_per_storehouse = reclimit or 2

    # models
    Storehouse = Model.get('storehouse')
    HarddiskLabel = Model.get('harddisk.label')

    # entries
    storehouses = Storehouse.find([])

    # create harddisk labels
    for i in range(1, len(storehouses) * harddisklabels_per_storehouse + 1):
        harddisk_label = HarddiskLabel()
        harddisk_label.save()
