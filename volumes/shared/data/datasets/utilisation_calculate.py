#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Calculate the utilization indicators
"""

# import random
# import decimal

from proteus import Model, Wizard

DEPENDS = [
    'tariff_relevance',
]


def generate(reclimit=0):

    # model
    Utilisation = Model.get('utilisation')

    # prepare dataset we depend upon
    utilisations = Utilisation.find([])

    # recalculate utilisation indicators
    for utilisation in utilisations:
        Wizard('utilisation.calculate', models=[utilisation])
