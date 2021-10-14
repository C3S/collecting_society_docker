#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff relevance of context objects
"""

from proteus import Model

DEPENDS = [
    'tariff_category',
    'utilisation'
]


def generate(reclimit=0):

    # models
    Tariff = Model.get('tariff_system.tariff')
    Location = Model.get('location')
    Event = Model.get('event')
    Release = Model.get('release')
    Website = Model.get('website')
    # TariffCategory = Model.get('tariff_system.category')
    # TariffRelevanceCategory = Model.get(
    #     'tariff_system.tariff.relevance.category')
    # TariffRelevance = Model.get('tariff_system.tariff.relevance')
    Utilisation = Model.get('utilisation')
    #
    # # entries
    # locations = Location.find([])
    # tariff_playing = Tariff.find([('category.code', '=', 'P')])[-1]
    # tariff_live = Tariff.find([('category.code', '=', 'L')])[-1]
    # tariff_reproduction = Tariff.find([('category.code', '=', 'C')])[-1]
    # tariff_online = Tariff.find([('category.code', '=', 'O')])[-1]
    # events = Event.find([])
    # releases = Release.find(['confirmed_copies', '>', 0])
    # websites = Website.find([])
    utilisations = Utilisation.find([])

    for utilisation in utilisations:
        if utilisation.tariff is None:
            pass
