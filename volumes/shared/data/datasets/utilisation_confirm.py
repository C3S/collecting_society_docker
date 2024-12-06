#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Calculate the utilization indicators
"""

import random
from decimal import Decimal as D

from proteus import Model, Wizard

DEPENDS = [
    'utilisation_calculate',
]


def generate(reclimit=0):

    # constants
    confirm_variation = 0.3

    # model
    Utilisation = Model.get('utilisation')

    # prepare dataset we depend upon
    utilisations = Utilisation.find([])

    # recalculate utilisation indicators
    for utilisation in utilisations:
        if utilisation.tariff.category.code == 'L':
            if 'estimated' in utilisation.context.name:
                continue
            wizard = Wizard('utilisation.confirm', models=[utilisation])
            wizard.form.attendants += random.randint(
                int(-wizard.form.attendants * confirm_variation),
                int(wizard.form.attendants * confirm_variation))
            wizard.form.turnover_tickets += (
                wizard.form.turnover_tickets * D(confirm_variation)
                * D(random.random() * 2 - 1)
            ).quantize(D('1.00'))
            wizard.form.turnover_benefit += (
                wizard.form.turnover_benefit * D(confirm_variation)
                * D(random.random() * 2 - 1)
            ).quantize(D('1.00'))
            wizard.form.expenses_musicians += (
                wizard.form.expenses_musicians * D(confirm_variation)
                * D(random.random() * 2 - 1)
            ).quantize(D('1.00'))
            wizard.form.expenses_production += (
                wizard.form.expenses_production * D(confirm_variation)
                * D(random.random() * 2 - 1)
            ).quantize(D('1.00'))
            wizard.execute('review_utilisation_indicators')
            wizard.execute('save')
        elif utilisation.tariff.category.code == 'C':
            pass
        elif utilisation.tariff.category.code == 'P':
            pass
        elif utilisation.tariff.category.code == 'O':
            pass
