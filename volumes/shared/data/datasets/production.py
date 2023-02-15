#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Finish minimal setup without demo data, tick config wizards
"""

from proteus import Model

DEPENDS = [
    'activate',
    'upgrade',
    'language',
    'currency',
    'country',
    'postal_code',
    'payment_term',
    'company',
    'company_employee',
    'user',
    'fiscal_year',
    'journal',
    'account_chart',
    'account_view',
    'product',
]


def generate(reclimit=0):

    # models
    Item = Model.get('ir.module.config_wizard.item')

    # entries
    items = Item.find()

    # configuration
    for item in items:
        item.state = 'done'
        item.save()
