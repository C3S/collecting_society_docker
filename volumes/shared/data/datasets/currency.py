#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Set the number of decimals for EUR
"""

from decimal import Decimal
from proteus import Model

DEPENDS = [
    'upgrade'
]


def generate():
    Currency = Model.get('currency.currency')
    euro, = Currency.find([('code', '=', 'EUR')])
    euro.rounding = Decimal('0.000001')
    euro.save()
