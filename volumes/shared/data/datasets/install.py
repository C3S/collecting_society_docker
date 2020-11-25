#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# For copyright and license terms, see COPYRIGHT.rst (top level of repository)
# Repository: https://github.com/C3S/collecting_society_docker

"""
Install module 'collecting_society'
"""

from proteus import Model

DEPENDS = []


def generate():
    Module = Model.get('ir.module.module')
    collecting_society_module, = Module.find(
        [('name', '=', 'collecting_society')])
    collecting_society_module.click('install')
