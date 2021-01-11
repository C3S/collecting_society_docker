#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Install the module 'collecting_society'
"""

from proteus import Model

DEPENDS = []


def generate(reclimit=0):

    # models
    Module = Model.get('ir.module.module')

    # entries
    collecting_society_module, = Module.find(
        [('name', '=', 'collecting_society')])

    # install
    collecting_society_module.click('install')
