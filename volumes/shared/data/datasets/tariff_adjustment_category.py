#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff adjustment categories
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar

DEPENDS = [
    'tariff_category',
]


def generate(reclimit=0):

    # models
    TariffCategory = Model.get('tariff_system.category')
    TariffAdjustmentCategory = Model.get(
        'tariff_system.tariff.adjustment.category')

    # create tariff adjustment categories
    path = os.path.join('data', 'csv', 'tariff_adjustment_category.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for row in reader:
            tcs = []
            for tc in row['tariff_categories'].split(","):
                tcs += TariffCategory.find(['code', '=', tc])
            TariffAdjustmentCategory(
                name=row['name'],
                value_min=float(row['value_min']),
                value_max=float(row['value_max']),
                value_default=float(row['value_default']),
                priority=int(row['priority']),
                operation=row['operation'],
                tariff_categories=tcs
            ).save()
