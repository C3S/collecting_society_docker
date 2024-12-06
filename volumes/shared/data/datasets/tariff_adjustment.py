#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff adjustments
"""

import random
# import decimal

from proteus import Model

DEPENDS = [
    'utilisation',
    'tariff_adjustment_category'
]


def generate(reclimit=0):

    # constants
    tariff_adjustment_in_utilisation_chance = .4

    # models
    Utilisation = Model.get('utilisation')
    TariffAdjustmentCategory = Model.get(
        'tariff_system.tariff.adjustment.category')

    # prepare datasets we depend upon
    utilisations = Utilisation.find([])
    tariff_adjustment_categories = TariffAdjustmentCategory.find([
        'code', '!=', 'missing_playlist_fee'
    ])

    for utilisation in utilisations:
        tariff_adjustment_categories_already_used = set()
        while tariff_adjustment_in_utilisation_chance < random.random():
            # add a random tariff adjustment
            adjucat = random.choice(tariff_adjustment_categories)
            if (adjucat.id not in tariff_adjustment_categories_already_used):
                status = random.choice(['approved', 'rejected'])
                # adjust status for estimated/confirmed utilisations
                if utilisation.tariff.category.code == 'L':
                    if 'estimated' in utilisation.context.name:
                        status = 'on_approval'
                    if 'confirmed' in utilisation.context.name:
                        status = random.choice(
                            ['on_approval', 'approved', 'rejected'])

                utilisation.estimated_adjustments.new(
                    category=adjucat,
                    status=status,
                    value=adjucat.value_default,
                    deviation=False,
                    deviation_reason=""
                )
                utilisation.save()
                tariff_adjustment_categories_already_used.add(adjucat.id)
