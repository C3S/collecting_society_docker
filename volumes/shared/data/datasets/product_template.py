#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the product templates
"""

from decimal import Decimal

from proteus import Model

DEPENDS = [
    'product_category',
]


def generate(reclimit=0):

    # models
    ProductCategory = Model.get('product.category')
    ProductTemplate = Model.get('product.template')
    ProductUom = Model.get('product.uom')

    # entries
    unit, = ProductUom.find(['name', '=', 'Stück'], limit=1)
    administration_category, = ProductCategory.find(
        ['name', '=', 'Administration Amount'], limit=1)
    distribution_category, = ProductCategory.find(
        ['name', '=', 'Distribution Amount'], limit=1)

    # create product templates
    administration = ProductTemplate()
    administration.name = "Administration Amount"
    administration.type = "service"
    administration.code = "A"
    administration.account_category = administration_category
    administration.default_uom = unit
    administration.list_price = Decimal(0)
    administration.cost_price = Decimal(0)
    administration.save()

    distribution = ProductTemplate()
    distribution.name = "Distribution Amount"
    distribution.type = "service"
    distribution.code = "D"
    distribution.account_category = distribution_category
    distribution.default_uom = unit
    distribution.list_price = Decimal(0)
    distribution.cost_price = Decimal(0)
    distribution.save()
