#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the tariff categories
"""

import os
import csv

from proteus import Model

from . import csv_delimiter, csv_quotechar

DEPENDS = [
    'production',
]


def generate(reclimit=0):

    # models
    Product = Model.get('product.product')
    TariffCategory = Model.get('tariff_system.category')

    # entries
    administration_product, = Product.find(['code', '=', 'A'])
    distribution_product, = Product.find(['code', '=', 'D'])

    # create tariff categories
    path = os.path.join('data', 'csv', 'tariff_category.csv')
    with open(path, 'r') as f:
        reader = csv.DictReader(
            f, delimiter=csv_delimiter, quotechar=csv_quotechar)
        for row in reader:
            TariffCategory(
                name=row['name'],
                code=row['code'],
                description=row['description'],
                administration_product=administration_product,
                distribution_product=distribution_product
            ).save()
