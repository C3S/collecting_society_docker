#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Import postal codes (DE), using import_postal_codes script
"""

from trytond.modules.country.scripts import import_postal_codes

DEPENDS = [
    'country',
]


def generate(reclimit=0):
    try:
        import_postal_codes.do_import(['de'])
    except Exception as e:
        print(e)
        print("Import of postal codes skipped.")
