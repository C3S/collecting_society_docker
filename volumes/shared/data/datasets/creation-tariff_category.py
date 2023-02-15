#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff categories for the creations
"""

import random

from proteus import Model

DEPENDS = [
    'creation',
    'collecting_society',
    'tariff_category',
]


def generate(reclimit=0):

    # models
    Creation = Model.get('creation')
    TariffCategory = Model.get('tariff_system.category')
    CreationTariffCategory = Model.get('creation-tariff_category')
    CollectingSociety = Model.get('collecting_society')

    # entries
    creations = Creation.find([('claim_state', '!=', 'unclaimed')])

    # create creation tariff categories
    for creation in creations:
        css = CollectingSociety.find([('represents_copyright', '=', True)])
        tariff_categories = TariffCategory.find([])
        samples = random.sample(
            tariff_categories, random.randint(1, len(tariff_categories)))
        for category in samples:
            CreationTariffCategory(
                creation=creation,
                category=category,
                collecting_society=random.choice(css)
            ).save()
