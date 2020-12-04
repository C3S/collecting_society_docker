#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Finish minimal setup without demo data, tick config wizards
"""

from proteus import Model

DEPENDS = [
    'install',
    'upgrade',
    'language',
    'currency',
    'payment_term',
    'company',
    'user',
    'fiscal_year',
    'journal',
    'account_chart',
    'account_view',
    'tax',
]


def generate():
    Item = Model.get('ir.module.module.config_wizard.item')
    items = Item.find()
    for item in items:
        item.state = 'done'
        item.save()