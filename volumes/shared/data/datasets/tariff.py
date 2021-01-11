#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariffs
"""

from proteus import Model

DEPENDS = [
    'tariff_system',
    'tariff_category',
]


def generate(reclimit=0):

    # models
    TariffSystem = Model.get('tariff_system')
    TariffCategory = Model.get('tariff_system.category')
    Tariff = Model.get('tariff_system.tariff')

    # Tariffs
    tariff_systems = TariffSystem.find([])
    tariff_categories = TariffCategory.find([])
    for system in tariff_systems:
        for category in tariff_categories:
            Tariff(
                system=system,
                category=category
            ).save()
