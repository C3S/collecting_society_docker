#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Execute upgrade wizard
"""

from proteus import Wizard

DEPENDS = [
    'install'
]


def generate():
    Wizard('ir.module.module.install_upgrade').execute('upgrade')
