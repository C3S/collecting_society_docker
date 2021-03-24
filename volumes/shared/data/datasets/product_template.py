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
    'account_chart',
]


def generate(reclimit=0):

    # models
    Account = Model.get('account.account')
    Tax = Model.get('account.tax')
    ProductTemplate = Model.get('product.template')
    ProductUom = Model.get('product.uom')

    # entries
    unit, = ProductUom.find(['name', '=', 'Unit'])
    account8400, = Account.find([('code', '=', "8400")])
    tax19, = Tax.find([('name', '=', "19% Umsatzsteuer")])
    tax0, = Tax.find([('name', '=', "nicht steuerbar")])

    # create product templates
    administration = ProductTemplate()
    administration.name = "Administration Amount"
    administration.type = "service"
    administration.default_uom = unit
    administration.list_price = Decimal(0)
    administration.cost_price = Decimal(0)
    administration.account_revenue = account8400
    administration.customer_taxes.extend([tax19])
    administration.save()

    distribution = ProductTemplate()
    distribution.name = "Distribution Amount"
    distribution.type = "service"
    distribution.default_uom = unit
    distribution.list_price = Decimal(0)
    distribution.cost_price = Decimal(0)
    distribution.account_revenue = account8400
    distribution.customer_taxes.extend([tax0])
    distribution.save()
