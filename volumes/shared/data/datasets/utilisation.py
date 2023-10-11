#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the utilizations
"""

import random
import decimal

from proteus import Model

DEPENDS = [
    'declaration'
]


def generate(reclimit=0):

    # model
    Utilisation = Model.get('utilisation')

    # prepare dataset we depend upon
    all_utilisations = Utilisation.find([])

    for each_util in all_utilisations:
        each_util.estimated_base = decimal.Decimal(round(
            random.randint(100, 10000)))  # add some calculation base amounts
        each_util.save()

    # TODO: add some more utilisations for declarations with recurring period
