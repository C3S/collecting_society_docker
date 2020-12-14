#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create tariff related data
"""

from proteus import  Model

import csv
import datetime

DEPENDS = [
    'master'
]


def generate(reclimit):

    # constants
    test_tariff_categories = '/shared/data/csv/tariff_categories.csv'
    test_tariff_adjustment_categories = '/shared/data/csv/tariff_adjustment_categories.csv'
    test_tariff_relevance_categories = '/shared/data/csv/tariff_relevance_categories.csv'
    delimiter = ','
    quotechar = '"'
    tariff_systems = reclimit or 3
    if tariff_systems < 2:
        tariff_systems = 2  # or licensee usecases would break

    # models
    TariffSystem = Model.get('tariff_system')
    TariffCategory = Model.get('tariff_system.category')
    TariffAdjustmentCategory = Model.get('tariff_system.tariff.adjustment.category')
    TariffRelevanceCategory = Model.get('tariff_system.tariff.relevance.category')
    Tariff = Model.get('tariff_system.tariff')

    # Tariff Systems
    today = datetime.date.today()
    for i in range(1, tariff_systems + 1):
        number = i
        TariffSystem(
            version="%s.0" % number,
            valid_from=today
        ).save()

    # Tariff Categories
    with open(test_tariff_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            TariffCategory(
                name=category['name'],
                code=category['code'],
                description=category['description']
            ).save()

    # Tariff Adjustment Categories
    with open(test_tariff_adjustment_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            tcs = []
            for tc in category['tariff_categories'].split(","):
                tcs += TariffCategory.find(['code', '=', tc])
            TariffAdjustmentCategory(
                name=category['name'],
                value_min=float(category['value_min']),
                value_max=float(category['value_max']),
                value_default=float(category['value_default']),
                priority=int(category['priority']),
                operation=category['operation'],
                tariff_categories=tcs
            ).save()

    # Tariff Relevance Categories
    with open(test_tariff_relevance_categories, 'r') as f:
        reader = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        i = 1
        for category in reader:
            i += 1
            tcs = []
            for tc in category['tariff_categories'].split(","):
                tcs += TariffCategory.find(['code', '=', tc])
            TariffRelevanceCategory(
                name=category['name'],
                value_min=float(category['value_min']),
                value_max=float(category['value_max']),
                value_default=float(category['value_default']),
                tariff_categories=tcs
            ).save()

    #Tariffs
    tariff_systems = TariffSystem.find([])
    tariff_categories = TariffCategory.find([])
    for system in tariff_systems:
        for category in tariff_categories:
            Tariff(
                system=system,
                category=category
            ).save()
