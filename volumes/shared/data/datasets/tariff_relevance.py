#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff relevance of utilisations
"""

import random
from proteus import Model

DEPENDS = [
    'tariff_category',
    'tariff_relevance_category',
    'utilisation'
]


def generate(reclimit=0):

    # models
    Tariff = Model.get('tariff_system.tariff')
    TariffRelevance = Model.get('tariff_system.tariff.relevance')
    Utilisation = Model.get('utilisation')

    # entries
    utilisations = Utilisation.find([])

    for utilisation in utilisations:
        utiltarcat = utilisation.tariff.category.code
        tariff_relevances = Tariff.find(
            [('category.code', '=', utiltarcat)])[-1]
        random_relevance_cat = random.choice(
            tariff_relevances.category.relevance_categories)
        if tariff_relevances.category:
            relevance = TariffRelevance()
            relevance.category = random_relevance_cat
            relevance.value = random_relevance_cat.value_default
            relevance.save()
            utilisation.estimated_relevance = relevance
            utilisation.save()
