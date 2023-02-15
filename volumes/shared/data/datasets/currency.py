#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Import and translate currencies, using import_currencies script
"""

from trytond.modules.currency.scripts import import_currencies

DEPENDS = [
    'language',
]


def generate(reclimit=0):
    import_currencies.do_import()
