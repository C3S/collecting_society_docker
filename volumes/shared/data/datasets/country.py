#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Import and translate countries and subdivisions, using import_countries script
"""

from trytond.modules.country.scripts import import_countries

DEPENDS = [
    'language',
]


def generate(reclimit=0):
    import_countries.do_import()
