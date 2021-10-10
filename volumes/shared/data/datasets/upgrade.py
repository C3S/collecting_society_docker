#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Execute the upgrade wizard
"""

from proteus import Wizard

DEPENDS = [
    'activate',
]


def generate(reclimit=0):

    # wizards
    activate_upgrade = Wizard('ir.module.activate_upgrade')

    # upgrade
    activate_upgrade.execute('upgrade')
