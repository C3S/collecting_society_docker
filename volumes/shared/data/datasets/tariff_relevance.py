#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff relevance of context objects
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
    Location = Model.get('location')
    Event = Model.get('event')
    Release = Model.get('release')
    Website = Model.get('website')
    TariffCategory = Model.get('tariff_system.category')
    TariffRelevanceCategory = Model.get(
        'tariff_system.tariff.relevance.category')
    TariffRelevance = Model.get('tariff_system.tariff.relevance')
    Utilisation = Model.get('utilisation')

    # entries
    # locations = Location.find([])
    # tariff_playing = Tariff.find([('category.code', '=', 'P')])[-1]
    # tariff_live = Tariff.find([('category.code', '=', 'L')])[-1]
    # tariff_reproduction = Tariff.find([('category.code', '=', 'C')])[-1]
    # tariff_online = Tariff.find([('category.code', '=', 'O')])[-1]
    # events = Event.find([])
    # releases = Release.find(['confirmed_copies', '>', 0])
    # websites = Website.find([])
    tariff_relevance_categories = TariffRelevanceCategory.find([])
    tariff_categories = TariffCategory.find([])
    utilisations = Utilisation.find([])

    # for utilisation in utilisations:
    #     utiltarcat = utilisation.tariff.category.code
    #     tariff_relevances = Tariff.find(
    #         [('category.code', '=', utiltarcat)])[-1]
    #     random_relevance_cat = random.choice(
    #         tariff_relevances.category.relevance_categories)
    #     if tariff_relevances.category:
    #         relevance = TariffRelevance()
    #         relevance.category = random_relevance_cat
    #         relevance.value = random_relevance_cat.value_default
    #         relevance.save()
    #         utilisation.estimated_relevance = relevance.id
    #         utilisation.save()
