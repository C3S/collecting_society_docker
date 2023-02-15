#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Create the product categories
"""

from proteus import Model

DEPENDS = [
    'account_chart',
]


def generate(reclimit=0):

    # models
    Account = Model.get('account.account')
    Tax = Model.get('account.tax')
    ProductCategory = Model.get('product.category')

    # entries
    account8400, = Account.find([('code', '=', "8400")], limit=1)
    tax19, = Tax.find([('name', '=', "Umsatzsteuer – Normalsatz")], limit=1)
    tax0, = Tax.find([('name', '=', "nicht steuerbar")], limit=1)

    # create product categories
    administration = ProductCategory()
    administration.accounting = True
    administration.name = "Administration Amount"
    administration.account_revenue = account8400
    administration.customer_taxes.append(tax19)
    administration.save()

    distribution = ProductCategory()
    distribution.accounting = True
    distribution.name = "Distribution Amount"
    distribution.account_revenue = account8400
    distribution.customer_taxes.append(tax0)
    distribution.save()
