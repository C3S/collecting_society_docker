#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Execute the upgrade wizard
"""

from proteus import Wizard

DEPENDS = [
    'install',
]


def generate(reclimit=0):

    # wizards
    install_upgrade = Wizard('ir.module.module.install_upgrade')

    # upgrade
    install_upgrade.execute('upgrade')
