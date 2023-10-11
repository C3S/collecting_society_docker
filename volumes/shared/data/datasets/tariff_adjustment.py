#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff adjustments
"""

import random
import decimal

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
    # TariffAdjustment = Model.get('tariff_system.tariff.adjustment')
    TariffAdjustmentCategory = Model.get(
        'tariff_system.tariff.adjustment.category')

    # prepare datasets we depend upon
    all_utilisations = Utilisation.find([])
    all_tariff_adjustment_categories = TariffAdjustmentCategory.find([])

    for each_util in all_utilisations:
        tariff_adjustment_categories_already_used = set()
        while tariff_adjustment_in_utilisation_chance < random.random():
            # add a random tariff adjustment
            adjucat = random.choice(all_tariff_adjustment_categories)
            if (adjucat.id not in tariff_adjustment_categories_already_used):
                each_util.estimated_adjustments.new(
                    category=adjucat,
                    status=random.choice(['on_approval', 'approved']),
                    value=adjucat.value_default,
                    deviation=False,
                    deviation_reason=""
                )
                each_util.save()
                tariff_adjustment_categories_already_used.add(adjucat.id)
